from flask import Flask, render_template, request, jsonify, redirect
import os
import json
from datetime import datetime
from collections import Counter, defaultdict

app = Flask(__name__)

LOGS_DIR = 'visitors_logs'
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)
    print(f"📁 Создана папка для логов: {LOGS_DIR}")

COMBO_IDS = {
    ("процветание", "процветание", "процветание", "процветание"): "GOOD_1",
    ("процветание", "процветание", "процветание", "стагнация"): "GOOD_2",
    ("процветание", "процветание", "процветание", "кризис"): "GOOD_3",
    ("процветание", "процветание", "стагнация", "процветание"): "GOOD_4",
    ("процветание", "стагнация", "процветание", "процветание"): "GOOD_5",
    ("стагнация", "процветание", "процветание", "процветание"): "GOOD_6",
    ("кризис", "процветание", "процветание", "процветание"): "GOOD_7",
    ("процветание", "кризис", "процветание", "процветание"): "GOOD_8",
    ("стагнация", "процветание", "процветание", "стагнация"): "GOOD_9",
    ("процветание", "процветание", "стагнация", "стагнация"): "GOOD_10",

    ("процветание", "процветание", "стагнация", "кризис"): "MEDIUM_1",
    ("процветание", "процветание", "кризис", "процветание"): "MEDIUM_2",
    ("процветание", "процветание", "кризис", "стагнация"): "MEDIUM_3",
    ("процветание", "процветание", "кризис", "кризис"): "MEDIUM_4",
    ("процветание", "стагнация", "процветание", "стагнация"): "MEDIUM_5",
    ("процветание", "стагнация", "процветание", "кризис"): "MEDIUM_6",
    ("процветание", "стагнация", "стагнация", "процветание"): "MEDIUM_7",
    ("процветание", "стагнация", "стагнация", "стагнация"): "MEDIUM_8",
    ("процветание", "стагнация", "стагнация", "кризис"): "MEDIUM_9",
    ("процветание", "стагнация", "кризис", "процветание"): "MEDIUM_10",
    ("процветание", "стагнация", "кризис", "стагнация"): "MEDIUM_11",
    ("процветание", "стагнация", "кризис", "кризис"): "MEDIUM_12",
    ("процветание", "кризис", "процветание", "стагнация"): "MEDIUM_13",
    ("процветание", "кризис", "процветание", "кризис"): "MEDIUM_14",
    ("процветание", "кризис", "стагнация", "процветание"): "MEDIUM_15",
    ("процветание", "кризис", "стагнация", "стагнация"): "MEDIUM_16",
    ("процветание", "кризис", "стагнация", "кризис"): "MEDIUM_17",
    ("процветание", "кризис", "кризис", "процветание"): "MEDIUM_18",
    ("процветание", "кризис", "кризис", "стагнация"): "MEDIUM_19",
    ("стагнация", "процветание", "процветание", "кризис"): "MEDIUM_20",
    ("стагнация", "процветание", "стагнация", "процветание"): "MEDIUM_21",
    ("стагнация", "процветание", "стагнация", "стагнация"): "MEDIUM_22",
    ("стагнация", "процветание", "стагнация", "кризис"): "MEDIUM_23",
    ("стагнация", "процветание", "кризис", "процветание"): "MEDIUM_24",
    ("стагнация", "процветание", "кризис", "стагнация"): "MEDIUM_25",
    ("стагнация", "процветание", "кризис", "кризис"): "MEDIUM_26",
    ("стагнация", "стагнация", "процветание", "процветание"): "MEDIUM_27",
    ("стагнация", "стагнация", "процветание", "стагнация"): "MEDIUM_28",
    ("стагнация", "стагнация", "процветание", "кризис"): "MEDIUM_29",
    ("стагнация", "стагнация", "стагнация", "процветание"): "MEDIUM_30",
    ("стагнация", "стагнация", "стагнация", "стагнация"): "MEDIUM_31",
    ("стагнация", "стагнация", "стагнация", "кризис"): "MEDIUM_32",
    ("стагнация", "стагнация", "кризис", "процветание"): "MEDIUM_33",
    ("стагнация", "стагнация", "кризис", "стагнация"): "MEDIUM_34",
    ("стагнация", "стагнация", "кризис", "кризис"): "MEDIUM_35",
    ("стагнация", "кризис", "процветание", "процветание"): "MEDIUM_36",
    ("стагнация", "кризис", "процветание", "стагнация"): "MEDIUM_37",
    ("стагнация", "кризис", "процветание", "кризис"): "MEDIUM_38",
    ("стагнация", "кризис", "стагнация", "процветание"): "MEDIUM_39",
    ("стагнация", "кризис", "стагнация", "стагнация"): "MEDIUM_40",
    ("стагнация", "кризис", "стагнация", "кризис"): "MEDIUM_41",
    ("стагнация", "кризис", "кризис", "процветание"): "MEDIUM_42",
    ("стагнация", "кризис", "кризис", "стагнация"): "MEDIUM_43",
    ("стагнация", "кризис", "кризис", "кризис"): "MEDIUM_44",
    ("кризис", "процветание", "процветание", "стагнация"): "MEDIUM_45",
    ("кризис", "процветание", "процветание", "кризис"): "MEDIUM_46",
    ("кризис", "процветание", "стагнация", "процветание"): "MEDIUM_47",
    ("кризис", "процветание", "стагнация", "стагнация"): "MEDIUM_48",
    ("кризис", "процветание", "стагнация", "кризис"): "MEDIUM_49",
    ("кризис", "процветание", "кризис", "процветание"): "MEDIUM_50",
    ("кризис", "процветание", "кризис", "стагнация"): "MEDIUM_51",
    ("кризис", "процветание", "кризис", "кризис"): "MEDIUM_52",
    ("кризис", "стагнация", "процветание", "процветание"): "MEDIUM_53",
    ("кризис", "стагнация", "процветание", "стагнация"): "MEDIUM_54",
    ("кризис", "стагнация", "процветание", "кризис"): "MEDIUM_55",
    ("кризис", "стагнация", "стагнация", "процветание"): "MEDIUM_56",
    ("кризис", "стагнация", "стагнация", "стагнация"): "MEDIUM_57",

    # BAD - 17 комбинаций (все остальные)
    ("процветание", "кризис", "кризис", "кризис"): "BAD_1",
    ("стагнация", "стагнация", "кризис", "кризис"): "BAD_2",
    ("стагнация", "кризис", "кризис", "кризис"): "BAD_3",
    ("кризис", "процветание", "кризис", "кризис"): "BAD_4",
    ("кризис", "стагнация", "стагнация", "кризис"): "BAD_5",
    ("кризис", "стагнация", "кризис", "процветание"): "BAD_6",
    ("кризис", "стагнация", "кризис", "стагнация"): "BAD_7",
    ("кризис", "стагнация", "кризис", "кризис"): "BAD_8",
    ("кризис", "кризис", "процветание", "процветание"): "BAD_9",
    ("кризис", "кризис", "процветание", "стагнация"): "BAD_10",
    ("кризис", "кризис", "процветание", "кризис"): "BAD_11",
    ("кризис", "кризис", "стагнация", "процветание"): "BAD_12",
    ("кризис", "кризис", "стагнация", "стагнация"): "BAD_13",
    ("кризис", "кризис", "стагнация", "кризис"): "BAD_14",
    ("кризис", "кризис", "кризис", "процветание"): "BAD_15",
    ("кризис", "кризис", "кризис", "стагнация"): "BAD_16",
    ("кризис", "кризис", "кризис", "кризис"): "BAD_17",
}

COMBO_DATA = {
    "GOOD_1": {"state": "green",
               "comment": "Система в точке идеального равновесия. Все макропоказатели в фазе устойчивого роста."},
    "GOOD_2": {"state": "green",
               "comment": "Фиксируем фазу экспансии. Стагнация индекса счастья не является критическим фактором."},
    "GOOD_3": {"state": "green",
               "comment": "Несмотря на кризис настроений, фундаментальные показатели подтверждают статус процветания."},
    "GOOD_4": {"state": "green",
               "comment": "Незначительное замедление ВВП компенсируется высокой доходностью. Фон благоприятный."},
    "GOOD_5": {"state": "green",
               "comment": "Стагнация доходов не препятствует росту. Текущая модель демонстрирует высокую эффективность."},
    "GOOD_6": {"state": "green",
               "comment": "Стабилизация на пике. Необходим мониторинг для защиты позиций от возможного перехода к спаду"},
    "GOOD_7": {"state": "green",
               "comment": "Сохранение фазы процветания при нарастающих инфляционных рисках. Система демонстрирует высокую адаптивность к внешним шокам"},
    "GOOD_8": {"state": "green",
               "comment": "Устойчивый профицит ВВП нивелирует риски социального сектора. Система удерживается в целевом диапазоне"},
    "GOOD_9": {"state": "green",
               "comment": "Стабилизация инфляции при высоких темпах роста подтверждает прочность текущего курса."},
    "GOOD_10": {"state": "green",
                "comment": "Индикаторы подтверждают продолжение цикла роста. Риски на текущий момент минимальны."},
    "MEDIUM_1": {"state": "yellow",
                 "comment": "Наблюдается торможение темпов роста. Система переходит в фазу инерционного движения."},
    "MEDIUM_2": {"state": "yellow",
                 "comment": "Кризис индекса счастья в сочетании с застоем ВВП требует пересмотра стимулирующей политики."},
    "MEDIUM_3": {"state": "yellow",
                 "comment": "Кризис производства при сохранении доходов переводит систему в режим ожидания."},
    "MEDIUM_4": {"state": "yellow",
                 "comment": "Динамика отсутствует. Эквалайзер фиксирует затяжной период низкой волатильности."},
    "MEDIUM_5": {"state": "yellow",
                 "comment": "Падение индекса счастья на фоне застоя ВВП указывает на системную усталость экономики."},
    "MEDIUM_6": {"state": "yellow",
                 "comment": "Текущие темпы развития признаны недостаточными. Фиксируем стагнацию индикаторов."},
    "MEDIUM_7": {"state": "yellow",
                 "comment": "Ключевые параметры замерли в среднем положении. Драйверы дальнейшего роста не выявлены."},
    "MEDIUM_8": {"state": "yellow",
                 "comment": "Совокупность социального пессимизма и отсутствия роста формирует негативный тренд."},
    "MEDIUM_9": {"state": "yellow",
                 "comment": "Кризис ВВП демпфируется низкой инфляцией, что удерживает систему от рецессии."},
    "MEDIUM_10": {"state": "yellow",
                  "comment": "Фиксируем стабилизацию на низких уровнях. Потенциал для рывка в текущих условиях исчерпан."},
    "MEDIUM_11": {"state": "yellow",
                  "comment": "Критическое охлаждение экономики. Переход к аналитической фазе для поиска точек роста в условиях дефицита активности"},
    "MEDIUM_12": {"state": "yellow",
                  "comment": "Снижение доходов при стагнации ВВП — сигнал к переходу на консервативную модель управления."},
    "MEDIUM_13": {"state": "yellow",
                  "comment": "Система удерживается за счет производства. Социальные индикаторы находятся в зоне риска."},
    "MEDIUM_14": {"state": "yellow",
                  "comment": "Хрупкое равновесие. Экономика балансирует на грани стагнации и перехода к спаду."},
    "MEDIUM_15": {"state": "yellow",
                  "comment": "Полное отсутствие волатильности. Рынок находится в состоянии статистического покоя."},
    "MEDIUM_16": {"state": "yellow",
                  "comment": "Критическое падение платежеспособного спроса и социальных ожиданий. Модель требует коренной трансформации."},
    "MEDIUM_17": {"state": "yellow",
                  "comment": "Отсутствие ценового давления не компенсирует общий упадок социального оптимизма."},
    "MEDIUM_18": {"state": "yellow",
                  "comment": "Синхронное замедление индикаторов. Система вошла в зону долгосрочного застоя."},
    "MEDIUM_19": {"state": "yellow",
                  "comment": "Экономический эквалайзер не фиксирует движения активов. Стагнация подтверждена."},
    "MEDIUM_20": {"state": "yellow",
                  "comment": "Социальный кризис блокирует возможности для восстановления инвестиционной активности."},
    "MEDIUM_21": {"state": "yellow",
                  "comment": "ВВП в глубокой просадке, но накопленный запас доходов удерживает систему от коллапса."},
    "MEDIUM_22": {"state": "yellow",
                  "comment": "Макроэкономические параметры сигнализируют о системном охлаждении всех рынков."},
    "MEDIUM_23": {"state": "yellow",
                  "comment": "Критическое снижение ВВП и уровня общественного благосостояния. Система находится в зоне глубокого спада"},
    "MEDIUM_24": {"state": "yellow",
                  "comment": "Застой доходов и цен. Система функционирует в режиме жесткой экономии ресурсов."},
    "MEDIUM_25": {"state": "yellow",
                  "comment": "Фиксируем отсутствие прогресса по ключевым направлениям. Динамика близка к нулевой."},
    "MEDIUM_26": {"state": "yellow",
                  "comment": "Общее снижение показателей при сохранении структуры. Состояние устойчивой стагнации."},
    "MEDIUM_27": {"state": "yellow",
                  "comment": "Остановка роста производства. Система достигла предела текущей технологической модели."},
    "MEDIUM_28": {"state": "yellow",
                  "comment": "Нулевая волатильность цен и объемов. Рынок пребывает в фазе длительного ожидания."},
    "MEDIUM_29": {"state": "yellow",
                  "comment": "Кризис социального самочувствия на фоне застоя лишает систему перспектив развития."},
    "MEDIUM_30": {"state": "yellow",
                  "comment": "Затяжная стагнация как результат инфляционного давления и промышленного спада. Рынок стабилизировался на депрессивных значениях"},
    "MEDIUM_31": {"state": "yellow",
                  "comment": "Кризис реальных доходов населения — основной сдерживающий фактор для растущего ВВП."},
    "MEDIUM_32": {"state": "yellow",
                  "comment": "Ухудшение показателей доходов переводит экономику в режим отрицательной стагнации."},
    "MEDIUM_33": {"state": "yellow",
                  "comment": "Индикаторы системы демонстрируют нисходящий тренд. Застой переходит в фазу спада."},
    "MEDIUM_34": {"state": "yellow",
                  "comment": "Рост цен провоцирует охлаждение спроса. Система находится в состоянии нестабильности."},
    "MEDIUM_35": {"state": "yellow",
                  "comment": "Высокая инфляция привела к социальному кризису. Требуется корректировка курса ДКП."},
    "MEDIUM_36": {"state": "yellow",
                  "comment": "Инфляционный шок замедлил темпы ВВП. Прогнозируем переход к затяжной стагнации."},
    "MEDIUM_37": {"state": "yellow",
                  "comment": "Стагфляционные процессы: цены растут при полном отсутствии экономического развития."},
    "MEDIUM_38": {"state": "yellow",
                  "comment": "Совокупный кризис настроений и инфляции. Покупательная способность под угрозой."},
    "MEDIUM_39": {"state": "yellow",
                  "comment": "Ценовая дестабилизация сменилась инертным состоянием реального сектора. Рецессия переросла в структурную стагнацию"},
    "MEDIUM_40": {"state": "yellow",
                  "comment": "Терминальная фаза стагфляции: на фоне дефицита капитала рыночные механизмы перешли в режим минимального функционирования"},
    "MEDIUM_41": {"state": "yellow",
                  "comment": "Рост ВВП полностью нивелируется агрессивной инфляцией. Чистый эффект — нулевой."},
    "MEDIUM_42": {"state": "yellow",
                  "comment": "Рост цен при застое доходов населения. Наблюдается снижение качества жизни."},
    "MEDIUM_43": {"state": "yellow",
                  "comment": "Эрозия капитала из-за инфляции на фоне глубокого социального пессимизма."},
    "MEDIUM_44": {"state": "yellow",
                  "comment": "Ценовое давление при стагнации производства ставит под вопрос устойчивость рынка."},
    "MEDIUM_45": {"state": "yellow",
                  "comment": "Стагнация как результат макроэкономического спада. Отсутствие производственной динамики на фоне ценовой нестабильности"},
    "MEDIUM_46": {"state": "yellow",
                  "comment": "Сочетание инфляционного и доходного кризисов удерживает рынок в депрессии."},
    "MEDIUM_47": {"state": "yellow",
                  "comment": "Ухудшение условий ведения бизнеса и падение уровня жизни. Система деградирует."},
    "MEDIUM_48": {"state": "yellow",
                  "comment": "Параметры находятся на критических отметках. Риск перехода в рецессию максимален."},
    "MEDIUM_49": {"state": "yellow",
                  "comment": "Кризис перепроизводства при инфляционном шоке. Рынок полностью разбалансирован."},
    "MEDIUM_50": {"state": "yellow",
                  "comment": "Стагнация производства на фоне ценовой стабильности. Требуется немедленное государственное регулирование."},
    "MEDIUM_51": {"state": "yellow",
                  "comment": "Кризис производства и доходов. Экономический цикл вошел в фазу системного разрушения."},
    "MEDIUM_52": {"state": "yellow",
                  "comment": "Переход инфляции в зону риска начинает разрушать общую стабильность системы."},
    "MEDIUM_53": {"state": "yellow",
                  "comment": "Кризис реальных доходов на фоне стагнации. Покупательная способность падает."},
    "MEDIUM_54": {"state": "yellow",
                  "comment": "Инфляционное давление сдерживает инвестиции. Экономика в подвешенном состоянии."},
    "MEDIUM_55": {"state": "yellow",
                  "comment": "Социальная напряжённость растёт из-за отсутствия прогресса. Нужны реформы."},
    "MEDIUM_56": {"state": "yellow", "comment": "Экономика застряла в болоте стагнации. Выход не просматривается."},
    "MEDIUM_57": {"state": "yellow",
                  "comment": "Критическая точка невозврата. Если не принять меры — скатываемся в кризис."},

    # BAD - 17 комбинаций (существенные кризисные сценарии)
    "BAD_1": {"state": "red",
              "comment": "💀 Тотальный коллапс! Доходы обрушились, производство парализовано. Народ на улицах, экономика в коме."},
    "BAD_2": {"state": "red",
              "comment": "📉 Двойной кризис: инфляция зашкаливает, ВВП падает. Реальная зарплата тает на глазах. Инвесторы бегут из страны."},
    "BAD_3": {"state": "red",
              "comment": "🔥 Стагфляция в терминальной стадии! Цены растут как на дрожжах, заводы стоят. Правительство в растерянности."},
    "BAD_4": {"state": "red",
              "comment": "🏦 Банковский кризис! Денежная масса взорвалась, рубль рухнул. Сбережения населения обесценились."},
    "BAD_5": {"state": "red",
              "comment": "⚰️ Экономика в агонии. Социальные протесты парализовали страну. Международная помощь на грани срыва."},
    "BAD_6": {"state": "red",
              "comment": "📊 Промышленность рухнула на 15%. Безработица зашкаливает. Малый бизнес закрывается тысячами."},
    "BAD_7": {"state": "red",
              "comment": "💸 Гиперинфляция! Деньги теряют ценность каждый час. Бартер возвращается в повседневную жизнь."},
    "BAD_8": {"state": "red",
              "comment": "🏭 Деиндустриализация! Заводы-гиганты объявляют о банкротстве. Целые города становятся безработными."},
    "BAD_9": {"state": "red",
              "comment": "🌪️ Экономический ураган! Рынок обвалился на 40%. Пенсионеры теряют последние накопления."},
    "BAD_10": {"state": "red",
               "comment": "🛑 Полная остановка инвестиций. Капитал утекает за границу рекордными темпами. Будущее туманно."},
    "BAD_11": {"state": "red",
               "comment": "📈 Инфляционная спираль раскручена! Цены удвоились за квартал. Голодовки сотрясают регионы."},
    "BAD_12": {"state": "red",
               "comment": "💀 Рецессия переросла в депрессию. Потеряно 10 лет развития. Демографическая катастрофа усугубляется."},
    "BAD_13": {"state": "red",
               "comment": "🔥 Синдром 'потерянного десятилетия'. Экономика отброшена на 15 лет назад. Надежд на восстановление почти нет."},
    "BAD_14": {"state": "red",
               "comment": "⚡ Энергетический коллапс на фоне кризиса. Цены на ЖКХ взлетели, люди не могут платить."},
    "BAD_15": {"state": "red",
               "comment": "📉 ВВП обвалился на 20% за год. Бюджет пуст, армия и полиция не получают зарплату. Хаос нарастает."},
    "BAD_16": {"state": "red",
               "comment": "💸 Дефолт неизбежен. Международные резервы исчерпаны. Суверенные рейтинги на дне."},
    "BAD_17": {"state": "red",
               "comment": "☠️ Апокалипсис! Экономика разрушена полностью. Система не подлежит восстановлению в обозримом будущем."},
}


def save_visit_log(ip_address, user_agent, page=None, link_click=None):
    try:
        log_file = os.path.join(LOGS_DIR, 'all_visits.json')
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                visits = json.load(f)
        else:
            visits = []
        visit_data = {
            'timestamp': datetime.now().isoformat(),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M:%S'),
            'ip': ip_address,
            'user_agent': user_agent,
        }
        if link_click:
            visit_data['event_type'] = 'link_click'
            visit_data['link_name'] = link_click['name']
            visit_data['link_url'] = link_click['url']
            print(f"🔗 ПЕРЕХОД ПО ССЫЛКЕ: {link_click['name']}")
            print(f"   IP: {ip_address}")
            print(f"   URL: {link_click['url']}")
        else:
            visit_data['event_type'] = 'page_visit'
            visit_data['page'] = page if page else 'main'
            print(f"👤 ПОСЕЩЕНИЕ САЙТА: {ip_address}")
            print(f"   Время: {visit_data['timestamp']}")
            print(f"   Страница: {visit_data['page']}")
        print(f"   Браузер: {user_agent[:80]}...")
        print("-" * 50)
        visits.append(visit_data)
        if len(visits) > 10000:
            visits = visits[-10000:]
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(visits, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"❌ Ошибка при сохранении лога: {e}")
        return False


def calculate_economy(rate, money_supply, operations, subsidies):
    base_inflation = 7.0
    base_income = 90.0
    base_gdp = 100.0
    base_happiness = 55.0

    inflation_from_rate = -rate * 0.18
    income_from_rate = -rate * 0.28
    gdp_from_rate = -rate * 0.25
    happiness_from_rate = -rate * 0.20

    inflation_from_money = money_supply * 0.35
    income_from_money = money_supply * 0.08
    gdp_from_money = money_supply * 0.10
    happiness_from_money = money_supply * 0.05

    if money_supply > 50:
        misery_penalty = (money_supply - 50) * 0.15
        income_from_money -= misery_penalty
        happiness_from_money -= misery_penalty
        inflation_from_money += (money_supply - 50) * 0.10

    inflation_from_ops = operations * 0.07
    income_from_ops = operations * 0.19
    gdp_from_ops = operations * 0.20
    happiness_from_ops = operations * 0.20

    inflation_from_subsidies = subsidies * 0.09
    income_from_subsidies = subsidies * 0.30
    gdp_from_subsidies = subsidies * 0.16
    happiness_from_subsidies = subsidies * 0.26

    inflation = base_inflation + inflation_from_rate + inflation_from_money + inflation_from_ops + inflation_from_subsidies
    inflation = max(0, inflation)

    real_income = base_income + income_from_rate + income_from_money + income_from_ops + income_from_subsidies
    real_income = max(50, min(150, real_income))

    current_gdp = base_gdp + gdp_from_rate + gdp_from_money + gdp_from_ops + gdp_from_subsidies
    current_gdp = max(60, min(140, current_gdp))

    happiness = base_happiness + happiness_from_rate + happiness_from_money + happiness_from_ops + happiness_from_subsidies
    happiness = max(20, min(100, happiness))

    gdp_change = ((current_gdp - 100) / 100) * 100

    def get_inflation_state(inflation_value):
        if inflation_value <= 5:
            return "процветание"
        elif inflation_value <= 12:
            return "стагнация"
        else:
            return "кризис"

    def get_income_state(income_value):
        if income_value >= 105:
            return "процветание"
        elif income_value >= 85:
            return "стагнация"
        return "кризис"

    def get_gdp_state(gdp_change_value):
        if gdp_change_value >= 1.5:
            return "процветание"
        elif gdp_change_value >= -2.0:
            return "стагнация"
        return "кризис"

    def get_happiness_state(happiness_value):
        if happiness_value >= 72:
            return "процветание"
        elif happiness_value >= 45:
            return "стагнация"
        return "кризис"

    states = {
        "inflation": get_inflation_state(inflation),
        "income": get_income_state(real_income),
        "gdp": get_gdp_state(gdp_change),
        "happiness": get_happiness_state(happiness)
    }

    key = (states["inflation"], states["income"], states["gdp"], states["happiness"])

    if key not in COMBO_IDS:
        red_count = sum(1 for v in states.values() if v == "кризис")
        green_count = sum(1 for v in states.values() if v == "процветание")
        if red_count >= 3:
            combo_id = "BAD_17"
            combo_info = {"state": "red"}
        elif green_count >= 3:
            combo_id = "GOOD_1"
            combo_info = {"state": "green"}
        else:
            combo_id = "MEDIUM_1"
            combo_info = {"state": "yellow"}
    else:
        combo_id = COMBO_IDS[key]
        combo_info = COMBO_DATA.get(combo_id, {"state": "yellow"})

    overall_state = combo_info["state"]
    state_to_text = {"green": "Процветание", "yellow": "Стагнация", "red": "Кризис"}
    overall_text = state_to_text.get(overall_state, "Стагнация")
    state_to_score = {"green": 100, "yellow": 50, "red": 0}

    overall_score = (
            state_to_score[states["inflation"]] * 0.20 +
            state_to_score[states["income"]] * 0.30 +
            state_to_score[states["gdp"]] * 0.30 +
            state_to_score[states["happiness"]] * 0.20
    )
    overall_score = max(0, min(100, overall_score))

    return {
        "inflation": round(inflation, 1),
        "real_income": round(real_income, 1),
        "gdp_change": round(gdp_change, 1),
        "happiness": round(happiness, 1),
        "states": states,
        "overall_score": round(overall_score, 1),
        "overall_state": overall_state,
        "overall_text": overall_text,
        "combo_id": combo_id
    }


# -------------------- АНАЛИТИКА (встроенная) --------------------
def get_analytics_stats():
    log_file = os.path.join(LOGS_DIR, 'all_visits.json')
    if not os.path.exists(log_file):
        return None
    with open(log_file, 'r', encoding='utf-8') as f:
        visits = json.load(f)
    if not visits:
        return None

    total_visits = len([v for v in visits if v['event_type'] == 'page_visit'])
    total_clicks = len([v for v in visits if v['event_type'] == 'link_click'])
    unique_visitors = len({v['ip'] for v in visits if v['event_type'] == 'page_visit'})
    clickers = {v['ip'] for v in visits if v['event_type'] == 'link_click'}
    conversion = (len(clickers) / unique_visitors * 100) if unique_visitors else 0

    daily = defaultdict(lambda: {'visits': 0, 'clicks': 0})
    for v in visits:
        date = v['date']
        if v['event_type'] == 'page_visit':
            daily[date]['visits'] += 1
        else:
            daily[date]['clicks'] += 1

    link_stats = Counter()
    for v in visits:
        if v['event_type'] == 'link_click':
            link_stats[v['link_name']] += 1

    return {
        'total_visits': total_visits,
        'total_clicks': total_clicks,
        'unique_visitors': unique_visitors,
        'conversion_rate': round(conversion, 2),
        'visitors_who_clicked': len(clickers),
        'daily_stats': dict(daily),
        'link_stats': dict(link_stats),
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


@app.route('/')
def index():
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    save_visit_log(ip_address, user_agent, page='main')
    return render_template('index.html')


@app.route('/analytics')
def analytics_page():
    stats = get_analytics_stats()
    return render_template('analytics.html', stats=stats)


@app.route('/api/analytics')
def analytics_api():
    stats = get_analytics_stats()
    if stats:
        return jsonify(stats)
    return jsonify({"error": "No data"}), 404


@app.route('/redirect/<link_name>')
def redirect_link(link_name):
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    links = {
        'inflation': {'name': 'ИНФЛЯЦИЯ (Уровень цен)', 'url': 'https://ru.wikipedia.org/wiki/Инфляция'},
        'income': {'name': 'РЕАЛЬНЫЕ ДОХОДЫ НАСЕЛЕНИЯ', 'url': 'https://ru.wikipedia.org/wiki/Реальные_доходы'},
        'gdp': {'name': 'ВВП (Валовой внутренний продукт)',
                'url': 'https://ru.wikipedia.org/wiki/Валовой_внутренний_продукт'},
        'happiness': {'name': 'ИНДЕКС СЧАСТЬЯ / ИНФЛЯЦИОННЫЕ ОЖИДАНИЯ',
                      'url': 'https://ru.wikipedia.org/wiki/Международный_индекс_счастья'},
        'subsidies': {'name': 'СУБСИДИИ / ДОТАЦИИ', 'url': 'https://ru.wikipedia.org/wiki/Субсидия'},
        'operations': {'name': 'ОПЕРАЦИИ НА ОТКРЫТОМ РЫНКЕ (ОФЗ)',
                       'url': 'https://ru.wikipedia.org/wiki/Операции_на_открытом_рынке'},
        'money': {'name': 'ДЕНЕЖНАЯ МАССА (М2)', 'url': 'https://ru.wikipedia.org/wiki/Денежная_масса'},
        'rate': {'name': 'КЛЮЧЕВАЯ СТАВКА ЦБ РФ', 'url': 'https://ru.wikipedia.org/wiki/Ключевая_ставка_в_России'}
    }
    if link_name in links:
        save_visit_log(ip_address, user_agent, link_click=links[link_name])
        return redirect(links[link_name]['url'])
    else:
        return redirect('/')


@app.route('/update', methods=['POST'])
def update():
    try:
        data = request.get_json()
        rate = float(data.get('rate', 0))
        money_supply = float(data.get('money_supply', 0))
        operations = float(data.get('operations', 0))
        subsidies = float(data.get('subsidies', 0))
        result = calculate_economy(rate, money_supply, operations, subsidies)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/select-symbol', methods=['POST'])
def select_symbol():
    data = request.json
    print(f"🎮 Выбран символ: {data}")
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
