from flask import Flask, render_template, request, jsonify, redirect
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from collections import Counter, defaultdict

app = Flask(__name__)

# Создаем папку для логов если её нет
LOGS_DIR = 'visitors_logs'
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)
    print(f"📁 Создана папка для логов: {LOGS_DIR}")

COMBO_IDS = {
    ("green", "green", "green", "green"): "GOOD_1",
    ("green", "green", "green", "yellow"): "GOOD_2",
    ("green", "green", "green", "red"): "GOOD_3",
    ("green", "green", "yellow", "green"): "GOOD_4",
    ("green", "yellow", "green", "green"): "GOOD_5",
    ("green", "yellow", "green", "yellow"): "GOOD_6",
    ("green", "yellow", "green", "red"): "GOOD_7",
    ("green", "red", "green", "green"): "GOOD_8",
    ("yellow", "green", "green", "green"): "GOOD_9",
    ("yellow", "green", "green", "yellow"): "GOOD_10",

    ("green", "green", "yellow", "yellow"): "MEDIUM_1",
    ("green", "green", "yellow", "red"): "MEDIUM_2",
    ("green", "green", "red", "green"): "MEDIUM_3",
    ("green", "green", "red", "yellow"): "MEDIUM_4",
    ("green", "green", "red", "red"): "MEDIUM_5",
    ("green", "yellow", "yellow", "green"): "MEDIUM_6",
    ("green", "yellow", "yellow", "yellow"): "MEDIUM_7",
    ("green", "yellow", "yellow", "red"): "MEDIUM_8",
    ("green", "yellow", "red", "green"): "MEDIUM_9",
    ("green", "yellow", "red", "yellow"): "MEDIUM_10",
    ("green", "yellow", "red", "red"): "MEDIUM_11",
    ("green", "red", "green", "yellow"): "MEDIUM_12",
    ("green", "red", "green", "red"): "MEDIUM_13",
    ("green", "red", "yellow", "green"): "MEDIUM_14",
    ("green", "red", "yellow", "yellow"): "MEDIUM_15",
    ("green", "red", "yellow", "red"): "MEDIUM_16",
    ("green", "red", "red", "green"): "MEDIUM_17",
    ("green", "red", "red", "yellow"): "MEDIUM_18",
    ("yellow", "green", "green", "red"): "MEDIUM_19",
    ("yellow", "green", "yellow", "green"): "MEDIUM_20",
    ("yellow", "green", "yellow", "yellow"): "MEDIUM_21",
    ("yellow", "green", "yellow", "red"): "MEDIUM_22",
    ("yellow", "green", "red", "green"): "MEDIUM_23",
    ("yellow", "green", "red", "yellow"): "MEDIUM_24",
    ("yellow", "green", "red", "red"): "MEDIUM_25",
    ("yellow", "yellow", "green", "green"): "MEDIUM_26",
    ("yellow", "yellow", "green", "yellow"): "MEDIUM_27",
    ("yellow", "yellow", "green", "red"): "MEDIUM_28",
    ("yellow", "yellow", "yellow", "green"): "MEDIUM_29",
    ("yellow", "yellow", "yellow", "yellow"): "MEDIUM_30",
    ("yellow", "yellow", "yellow", "red"): "MEDIUM_31",
    ("yellow", "yellow", "red", "green"): "MEDIUM_32",
    ("yellow", "yellow", "red", "yellow"): "MEDIUM_33",
    ("yellow", "yellow", "red", "red"): "MEDIUM_34",
    ("yellow", "red", "green", "green"): "MEDIUM_35",
    ("yellow", "red", "green", "yellow"): "MEDIUM_36",
    ("yellow", "red", "green", "red"): "MEDIUM_37",
    ("yellow", "red", "yellow", "green"): "MEDIUM_38",
    ("yellow", "red", "yellow", "yellow"): "MEDIUM_39",
    ("yellow", "red", "yellow", "red"): "MEDIUM_40",
    ("yellow", "red", "red", "green"): "MEDIUM_41",
    ("yellow", "red", "red", "yellow"): "MEDIUM_42",
    ("yellow", "red", "red", "red"): "MEDIUM_43",
    ("red", "green", "green", "green"): "MEDIUM_44",
    ("red", "green", "green", "yellow"): "MEDIUM_45",
    ("red", "green", "green", "red"): "MEDIUM_46",
    ("red", "green", "yellow", "green"): "MEDIUM_47",
    ("red", "green", "yellow", "yellow"): "MEDIUM_48",
    ("red", "green", "yellow", "red"): "MEDIUM_49",
    ("red", "green", "red", "green"): "MEDIUM_50",
    ("red", "green", "red", "yellow"): "MEDIUM_51",
    ("red", "green", "red", "red"): "MEDIUM_52",
    ("red", "yellow", "green", "green"): "MEDIUM_53",
    ("red", "yellow", "green", "yellow"): "MEDIUM_54",
    ("red", "yellow", "green", "red"): "MEDIUM_55",
    ("red", "yellow", "yellow", "green"): "MEDIUM_56",
    ("red", "yellow", "yellow", "yellow"): "MEDIUM_57",

    ("green", "red", "red", "red"): "BAD_1",
    ("yellow", "green", "red", "red"): "BAD_2",
    ("yellow", "yellow", "red", "red"): "BAD_3",
    ("yellow", "red", "red", "red"): "BAD_4",
    ("red", "green", "red", "red"): "BAD_5",
    ("red", "yellow", "red", "red"): "BAD_6",
    ("red", "red", "green", "green"): "BAD_7",
    ("red", "red", "green", "yellow"): "BAD_8",
    ("red", "red", "green", "red"): "BAD_9",
    ("red", "red", "yellow", "green"): "BAD_10",
    ("red", "red", "yellow", "yellow"): "BAD_11",
    ("red", "red", "yellow", "red"): "BAD_12",
    ("red", "red", "red", "green"): "BAD_13",
    ("red", "red", "red", "yellow"): "BAD_14",
    ("red", "red", "red", "red"): "BAD_15",
    ("red", "yellow", "yellow", "red"): "BAD_16",
    ("red", "yellow", "red", "yellow"): "BAD_17",
    ("red", "yellow", "red", "green"): "BAD_18",
    ("red", "red", "yellow", "red"): "BAD_19",
    ("red", "red", "red", "yellow"): "BAD_20",
    ("red", "yellow", "yellow", "yellow"): "BAD_21",
    ("yellow", "red", "yellow", "red"): "BAD_22",
    ("red", "yellow", "yellow", "red"): "BAD_23",
    ("red", "red", "red", "green"): "BAD_24",
}

COMBO_DATA = {
    # GOOD - 10 комбинаций
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
               "comment": "Достигнуто плато процветания. Требуется мониторинг для удержания позиций на пике."},
    "GOOD_7": {"state": "green",
               "comment": "Отрицательная динамика социального сектора не влияет на общую макроэкономическую устойчивость."},
    "GOOD_8": {"state": "green",
               "comment": "Снижение реальных доходов купируется мощным ВВП. Экономика остается в зеленой зоне."},
    "GOOD_9": {"state": "green",
               "comment": "Стабилизация инфляции при высоких темпах роста подтверждает прочность текущего курса."},
    "GOOD_10": {"state": "green",
                "comment": "Индикаторы подтверждают продолжение цикла роста. Риски на текущий момент минимальны."},

    # MEDIUM - 47 комбинаций (сохранены все)
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
                  "comment": "Температура экономики ниже нормы. Требуется анализ причин депрессивного состояния рынка."},
    "MEDIUM_12": {"state": "yellow",
                  "comment": "Снижение доходов при стагнации ВВП — сигнал к переходу на консервативную модель управления."},
    "MEDIUM_13": {"state": "yellow",
                  "comment": "Система удерживается за счет производства. Социальные индикаторы находятся в зоне риска."},
    "MEDIUM_14": {"state": "yellow",
                  "comment": "Хрупкое равновесие. Экономика балансирует на грани стагнации и перехода к спаду."},
    "MEDIUM_15": {"state": "yellow",
                  "comment": "Полное отсутствие волатильности. Рынок находится в состоянии статистического покоя."},
    "MEDIUM_16": {"state": "yellow",
                  "comment": "Двойной кризис доходов и настроений делает текущую модель крайне неустойчивой."},
    "MEDIUM_17": {"state": "yellow",
                  "comment": "Рецессия ВВП при низкой инфляции. Ситуация требует оперативного вмешательства регулятора."},
    "MEDIUM_18": {"state": "yellow",
                  "comment": "Кризис производства и доходов. Экономический цикл вошел в фазу системного разрушения."},
    "MEDIUM_19": {"state": "yellow",
                  "comment": "Отсутствие ценового давления не компенсирует общий упадок социального оптимизма."},
    "MEDIUM_20": {"state": "yellow",
                  "comment": "Синхронное замедление индикаторов. Система вошла в зону долгосрочного застоя."},
    "MEDIUM_21": {"state": "yellow",
                  "comment": "Экономический эквалайзер не фиксирует движения активов. Стагнация подтверждена."},
    "MEDIUM_22": {"state": "yellow",
                  "comment": "Социальный кризис блокирует возможности для восстановления инвестиционной активности."},
    "MEDIUM_23": {"state": "yellow",
                  "comment": "ВВП в глубокой просадке, но накопленный запас доходов удерживает систему от коллапса."},
    "MEDIUM_24": {"state": "yellow",
                  "comment": "Макроэкономические параметры сигнализируют о системном охлаждении всех рынков."},
    "MEDIUM_25": {"state": "yellow",
                  "comment": "Падение ВВП и кризис индекса счастья подтверждают фазу глубокой депрессии."},
    "MEDIUM_26": {"state": "yellow",
                  "comment": "Застой доходов и цен. Система функционирует в режиме жесткой экономии ресурсов."},
    "MEDIUM_27": {"state": "yellow",
                  "comment": "Фиксируем отсутствие прогресса по ключевым направлениям. Динамика близка к нулевой."},
    "MEDIUM_28": {"state": "yellow",
                  "comment": "Общее снижение показателей при сохранении структуры. Состояние устойчивой стагнации."},
    "MEDIUM_29": {"state": "yellow",
                  "comment": "Остановка роста производства. Система достигла предела текущей технологической модели."},
    "MEDIUM_30": {"state": "yellow",
                  "comment": "Нулевая волатильность цен и объемов. Рынок пребывает в фазе длительного ожидания."},
    "MEDIUM_31": {"state": "yellow",
                  "comment": "Кризис социального самочувствия на фоне застоя лишает систему перспектив развития."},
    "MEDIUM_32": {"state": "yellow",
                  "comment": "Сочетание инфляционного шока и падения производства привело к обвалу рынка."},
    "MEDIUM_33": {"state": "yellow",
                  "comment": "Неконтролируемое снижение макропараметров. Прогноз на следующий квартал негативный."},
    "MEDIUM_34": {"state": "yellow",
                  "comment": "Глубокий кризис. Индикаторы системы находятся за пределами допустимых значений."},
    "MEDIUM_35": {"state": "yellow",
                  "comment": "Кризис реальных доходов населения — основной сдерживающий фактор для растущего ВВП."},
    "MEDIUM_36": {"state": "yellow",
                  "comment": "Ухудшение показателей доходов переводит экономику в режим отрицательной стагнации."},
    "MEDIUM_37": {"state": "yellow",
                  "comment": "Инфляционное давление при падении доходов формирует критически негативный фон."},
    "MEDIUM_38": {"state": "yellow",
                  "comment": "Индикаторы системы демонстрируют нисходящий тренд. Застой переходит в фазу спада."},
    "MEDIUM_39": {"state": "yellow",
                  "comment": "Фиксируем остановку экономических циклов. Рост в текущих условиях не прогнозируется."},
    "MEDIUM_40": {"state": "yellow",
                  "comment": "Отрицательная динамика доходов и ВВП привела к развитию масштабной рецессии."},
    "MEDIUM_41": {"state": "yellow",
                  "comment": "Инфляционный взрыв при парализованном производстве. Экономика в критическом состоянии."},
    "MEDIUM_42": {"state": "yellow",
                  "comment": "Наблюдается деградация рыночных механизмов. Требуются экстренные меры реанимации."},
    "MEDIUM_43": {"state": "yellow",
                  "comment": "Полное отсутствие внутренних ресурсов для восстановления. Системный коллапс."},
    "MEDIUM_44": {"state": "yellow",
                  "comment": "Переход инфляции в зону риска начинает разрушать общую стабильность системы."},
    "MEDIUM_45": {"state": "yellow",
                  "comment": "Рост цен провоцирует охлаждение спроса. Система находится в состоянии нестабильности."},
    "MEDIUM_46": {"state": "yellow",
                  "comment": "Высокая инфляция привела к социальному кризису. Требуется корректировка курса ДКП."},
    "MEDIUM_47": {"state": "yellow",
                  "comment": "Инфляционный шок замедлил темпы ВВП. Прогнозируем переход к затяжной стагнации."},
    "MEDIUM_48": {"state": "yellow",
                  "comment": "Стагфляционные процессы: цены растут при полном отсутствии экономического развития."},
    "MEDIUM_49": {"state": "yellow",
                  "comment": "Совокупный кризис настроений и инфляции. Покупательная способность под угрозой."},
    "MEDIUM_50": {"state": "yellow",
                  "comment": "Рост ВВП полностью нивелируется агрессивной инфляцией. Чистый эффект — нулевой."},
    "MEDIUM_51": {"state": "yellow",
                  "comment": "Рост цен при застое доходов населения. Наблюдается снижение качества жизни."},
    "MEDIUM_52": {"state": "yellow",
                  "comment": "Эрозия капитала из-за инфляции на фоне глубокого социального пессимизма."},
    "MEDIUM_53": {"state": "yellow",
                  "comment": "Ценовое давление при стагнации производства ставит под вопрос устойчивость рынка."},
    "MEDIUM_54": {"state": "yellow",
                  "comment": "Сочетание инфляционного и доходного кризисов удерживает рынок в депрессии."},
    "MEDIUM_55": {"state": "yellow",
                  "comment": "Ухудшение условий ведения бизнеса и падение уровня жизни. Система деградирует."},
    "MEDIUM_56": {"state": "yellow",
                  "comment": "Параметры находятся на критических отметках. Риск перехода в рецессию максимален."},
    "MEDIUM_57": {"state": "yellow",
                  "comment": "Кризис перепроизводства при инфляционном шоке. Рынок полностью разбалансирован."},

    # BAD - 24 комбинации (усиленные комментарии)
    "BAD_1": {"state": "red", "comment": "💀 Тотальный коллапс! Все системы разрушены. Экономика в коме."},
    "BAD_2": {"state": "red", "comment": "📉 Двойной кризис: инфляция зашкаливает, ВВП падает. Реальная зарплата тает на глазах."},
    "BAD_3": {"state": "red", "comment": "🔥 Стагфляция в терминальной стадии! Цены растут как на дрожжах, заводы стоят."},
    "BAD_4": {"state": "red", "comment": "🏦 Банковский кризис! Денежная масса взорвалась, рубль рухнул."},
    "BAD_5": {"state": "red", "comment": "⚰️ Экономика в агонии. Социальные протесты парализовали страну."},
    "BAD_6": {"state": "red", "comment": "📊 Промышленность рухнула на 15%. Безработица зашкаливает."},
    "BAD_7": {"state": "red", "comment": "💸 Гиперинфляция! Деньги теряют ценность каждый час."},
    "BAD_8": {"state": "red", "comment": "🏭 Деиндустриализация! Заводы-гиганты объявляют о банкротстве."},
    "BAD_9": {"state": "red", "comment": "🌪️ Экономический ураган! Рынок обвалился на 40%."},
    "BAD_10": {"state": "red", "comment": "🛑 Полная остановка инвестиций. Капитал утекает за границу."},
    "BAD_11": {"state": "red", "comment": "📈 Инфляционная спираль раскручена! Цены удвоились за квартал."},
    "BAD_12": {"state": "red", "comment": "💀 Рецессия переросла в депрессию. Потеряно 10 лет развития."},
    "BAD_13": {"state": "red", "comment": "🔥 Синдром 'потерянного десятилетия'. Экономика отброшена на 15 лет назад."},
    "BAD_14": {"state": "red", "comment": "⚡ Энергетический коллапс на фоне кризиса. Цены на ЖКХ взлетели."},
    "BAD_15": {"state": "red", "comment": "📉 ВВП обвалился на 20% за год. Бюджет пуст."},
    "BAD_16": {"state": "red", "comment": "💸 Дефолт неизбежен. Международные резервы исчерпаны."},
    "BAD_17": {"state": "red", "comment": "☠️ Апокалипсис! Экономика разрушена полностью."},
    "BAD_18": {"state": "red", "comment": "💀 Системный кризис. Восстановление невозможно в обозримом будущем."},
    "BAD_19": {"state": "red", "comment": "📉 Катастрофа! Все макроэкономические метрики обнулены."},
    "BAD_20": {"state": "red", "comment": "🔥 Экономика горит. Нужны экстренные меры."},
    "BAD_21": {"state": "red", "comment": "⚰️ Полный коллапс. Страна на грани выживания."},
    "BAD_22": {"state": "red", "comment": "💸 Денежная система разрушена. Бартер возвращается."},
    "BAD_23": {"state": "red", "comment": "🏭 Промышленность парализована. Армия безработных растёт."},
    "BAD_24": {"state": "red", "comment": "☠️ Терминальная стадия. Экономика не подлежит спасению."},
}


def save_visit_log(ip_address, user_agent, page=None, link_click=None):
    """Сохраняет информацию о посещении или переходе по ссылке в единый JSON файл"""
    try:
        log_file = os.path.join(LOGS_DIR, 'all_visits.json')

        # Загружаем существующие данные или создаем новый список
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                visits = json.load(f)
        else:
            visits = []

        # Создаем запись
        visit_data = {
            'timestamp': datetime.now().isoformat(),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M:%S'),
            'ip': ip_address,
            'user_agent': user_agent,
        }

        # Добавляем информацию в зависимости от типа события
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

        # Сохраняем только последние 10000 записей чтобы файл не разрастался
        if len(visits) > 10000:
            visits = visits[-10000:]

        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(visits, f, ensure_ascii=False, indent=2)

        return True
    except Exception as e:
        print(f"❌ Ошибка при сохранении лога: {e}")
        return False


def calculate_economy(rate, money_supply, operations, subsidies):
    """
    Рассчитывает экономические показатели на основе параметров политики
    с усиленным негативным эффектом при высокой денежной массе.

    Параметры:
    - rate: ключевая ставка (-100..100)
    - money_supply: денежная масса/эмиссия (-100..100)
    - operations: операции на открытом рынке (-100..100)
    - subsidies: субсидии и трансферты (-100..100)
    """

    # Базовые значения (нейтральный уровень)
    base_inflation = 7.0
    base_income = 90.0
    base_gdp = 100.0
    base_happiness = 55.0

    # ==================== 1. КЛЮЧЕВАЯ СТАВКА ====================
    inflation_from_rate = -rate * 0.12
    income_from_rate = -rate * 0.22
    gdp_from_rate = -rate * 0.20
    happiness_from_rate = -rate * 0.15

    # ==================== 2. ДЕНЕЖНАЯ МАССА (М2) — УСИЛЕННЫЙ НЕГАТИВ ====================
    # Базовое влияние эмиссии (умеренное)
    inflation_from_money = money_supply * 0.16
    income_from_money = money_supply * 0.18      # уменьшено, чтобы штраф был заметнее
    gdp_from_money = money_supply * 0.16         # уменьшено
    happiness_from_money = money_supply * 0.08

    # ===== ШТРАФ ЗА ВЫСОКУЮ ЭМИССИЮ (УСИЛЕННЫЙ) =====
    if money_supply > 50:
        # Первый порог (50-70) — умеренный перегрев
        if money_supply <= 70:
            overheat = (money_supply - 50) * 0.20
            inflation_from_money += overheat
            income_from_money -= overheat * 1.2
            happiness_from_money -= overheat * 1.2
        else:
            # Второй порог (>70) — жёсткий перегрев
            overheat_medium = 20 * 0.20  # за 50-70
            inflation_from_money += overheat_medium
            income_from_money -= overheat_medium * 1.2
            happiness_from_money -= overheat_medium * 1.2
            
            # Жёсткий штраф за 70-100
            severe_overheat = (money_supply - 70) * 0.35
            inflation_from_money += severe_overheat
            income_from_money -= severe_overheat * 1.5
            happiness_from_money -= severe_overheat * 1.5
            
            # Эффект на ВВП становится сильно отрицательным
            gdp_penalty = (money_supply - 70) * 0.25
            gdp_from_money -= gdp_penalty

    # ===== ШТРАФ ЗА ДЕФЛЯЦИЮ (сильное сокращение М2) =====
    if money_supply < -50:
        deflation_penalty = (abs(money_supply) - 50) * 0.12
        inflation_from_money -= deflation_penalty
        gdp_from_money -= deflation_penalty * 0.8
        income_from_money -= deflation_penalty * 0.6
        happiness_from_money -= deflation_penalty * 0.6

    # ==================== 3. ОПЕРАЦИИ НА ОТКРЫТОМ РЫНКЕ ====================
    inflation_from_ops = operations * 0.06
    income_from_ops = operations * 0.18
    gdp_from_ops = operations * 0.18
    happiness_from_ops = operations * 0.18

    # ==================== 4. СУБСИДИИ ====================
    inflation_from_subsidies = subsidies * 0.08
    income_from_subsidies = subsidies * 0.28
    gdp_from_subsidies = subsidies * 0.14
    happiness_from_subsidies = subsidies * 0.26

    # ==================== СУММИРУЕМ ====================
    inflation = base_inflation + inflation_from_rate + inflation_from_money + inflation_from_ops + inflation_from_subsidies
    real_income = base_income + income_from_rate + income_from_money + income_from_ops + income_from_subsidies
    current_gdp = base_gdp + gdp_from_rate + gdp_from_money + gdp_from_ops + gdp_from_subsidies
    happiness = base_happiness + happiness_from_rate + happiness_from_money + happiness_from_ops + happiness_from_subsidies

    # ==================== ОБРАТНЫЕ СВЯЗИ (УСИЛЕННЫЕ) ====================
    # 5. Высокая инфляция разрушает доверие и реальные доходы
    if inflation > 10:
        happiness_loss = (inflation - 10) * 1.5      # усилено
        happiness -= happiness_loss
        real_income -= (inflation - 10) * 0.4        # усилено
    elif inflation < 3:
        happiness_gain = (3 - inflation) * 0.8
        happiness += happiness_gain

    # 6. Эффект стагфляции (высокая инфляция + падение ВВП) — усилен
    if inflation > 10 and current_gdp < 95:
        stagflation_penalty = (inflation - 10) * 0.6
        real_income -= stagflation_penalty
        happiness -= 5
        current_gdp -= stagflation_penalty * 0.3   # дополнительное падение ВВП

    # 7. Эффект доверия: высокое счастье стимулирует экономику
    if happiness > 75:
        gdp_from_trust = (happiness - 75) * 0.1
        current_gdp += gdp_from_trust

    # ==================== ОГРАНИЧЕНИЯ ====================
    inflation = max(0, min(35, inflation))  # верхняя граница увеличена до 35
    real_income = max(30, min(150, real_income))  # нижняя граница снижена до 30
    current_gdp = max(40, min(140, current_gdp))  # нижняя граница снижена до 40
    happiness = max(10, min(100, happiness))  # нижняя граница снижена до 10

    gdp_change = ((current_gdp - 100) / 100) * 100

    # ==================== ОПРЕДЕЛЕНИЕ СОСТОЯНИЙ ====================
    def get_inflation_state(inflation_value):
        if inflation_value <= 5:
            return "green"
        elif inflation_value > 12:
            return "red"
        return "yellow"

    def get_income_state(income_value):
        if income_value >= 105:
            return "green"
        elif income_value >= 85:
            return "yellow"
        return "red"

    def get_gdp_state(gdp_change_value):
        if gdp_change_value >= 1.5:
            return "green"
        elif gdp_change_value >= -2.0:
            return "yellow"
        return "red"

    def get_happiness_state(happiness_value):
        if happiness_value >= 72:
            return "green"
        elif happiness_value >= 45:
            return "yellow"
        return "red"

    states = {
        "inflation": get_inflation_state(inflation),
        "income": get_income_state(real_income),
        "gdp": get_gdp_state(gdp_change),
        "happiness": get_happiness_state(happiness)
    }

    # ==================== ОПРЕДЕЛЕНИЕ КОМБИНАЦИИ ====================
    key = (states["inflation"], states["income"], states["gdp"], states["happiness"])

    global COMBO_IDS, COMBO_DATA

    if key not in COMBO_IDS:
        red_count = sum(1 for v in states.values() if v == "red")
        green_count = sum(1 for v in states.values() if v == "green")

        if red_count >= 3:
            combo_id = "FALLBACK_RED"
            combo_info = {"state": "red", "comment": "Критическое состояние системы! Требуются экстренные меры."}
        elif green_count >= 3:
            combo_id = "FALLBACK_GREEN"
            combo_info = {"state": "green", "comment": "Экономика демонстрирует устойчивый рост."}
        else:
            combo_id = "FALLBACK_YELLOW"
            combo_info = {"state": "yellow", "comment": "Экономика в состоянии неопределённости."}
    else:
        combo_id = COMBO_IDS[key]
        combo_info = COMBO_DATA.get(combo_id, {"state": "yellow", "comment": "Ситуация неопределённая."})

    overall_state = combo_info["state"]

    state_to_text = {
        "green": "Процветание",
        "yellow": "Стагнация",
        "red": "Кризис"
    }
    overall_text = state_to_text.get(overall_state, "Стагнация")

    # ==================== ОБЩАЯ ОЦЕНКА ====================
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
        "overall_comment": combo_info.get("comment", "Ситуация стабильная."),
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
        'inflation': {
            'name': 'ИНФЛЯЦИЯ (Уровень цен)',
            'url': 'https://ru.wikipedia.org/wiki/Инфляция'
        },
        'income': {
            'name': 'РЕALЬНЫЕ ДОХОДЫ НАСЕЛЕНИЯ',
            'url': 'https://ru.wikipedia.org/wiki/Реальные_доходы'
        },
        'gdp': {
            'name': 'ВВП (Валовой внутренний продукт)',
            'url': 'https://ru.wikipedia.org/wiki/Валовой_внутренний_продукт'
        },
        'happiness': {
            'name': 'ИНДЕКС СЧАСТЬЯ / ИНФЛЯЦИОННЫЕ ОЖИДАНИЯ',
            'url': 'https://ru.wikipedia.org/wiki/Международный_индекс_счастья'
        },
        'subsidies': {
            'name': 'СУБСИДИИ / ДОТАЦИИ',
            'url': 'https://ru.wikipedia.org/wiki/Субсидия'
        },
        'operations': {
            'name': 'ОПЕРАЦИИ НА ОТКРЫТОМ РЫНКЕ (ОФЗ)',
            'url': 'https://ru.wikipedia.org/wiki/Операции_на_открытом_рынке'
        },
        'money': {
            'name': 'ДЕНЕЖНАЯ МАССА (М2)',
            'url': 'https://ru.wikipedia.org/wiki/Денежная_масса'
        },
        'rate': {
            'name': 'КЛЮЧЕВАЯ СТАВКА ЦБ РФ',
            'url': 'https://ru.wikipedia.org/wiki/Ключевая_ставка_в_России'
        }
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

@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        # Настройки для Mail.ru (замени на свои)
        SMTP_SERVER = "smtp.mail.ru"
        SMTP_PORT = 465
        SMTP_USERNAME = "economicequalizer@mail.ru"      # твой полный email
        SMTP_PASSWORD = "T2A8dfixgYcNyLpu6OC9"       # пароль для внешнего приложения
        RECIPIENT_EMAIL = "economicequalizer@mail.ru"    # куда отправлять
        
        # Формируем письмо
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = 'Обратная связь от Экономического эквалайзера'
        
        body = f"""
        <html>
        <body>
        <h3>Новое сообщение от пользователя</h3>
        <p><strong>Время:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Сообщение:</strong></p>
        <p>{message}</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html', 'utf-8'))
        
        # Отправка через SSL (порт 465)
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        
        print(f"Письмо отправлено: {message[:50]}...")
        return jsonify({"status": "ok"})
        
    except Exception as e:
        print(f"Ошибка отправки: {e}")
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
