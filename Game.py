from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

COMBO_IDS = {
    ("green", "green", "green", "green"): "GOD_1",
    ("green", "green", "green", "yellow"): "GOD_2",
    ("green", "green", "green", "red"): "GOD_3",
    ("green", "green", "yellow", "green"): "GOD_4",
    ("green", "yellow", "green", "green"): "GOD_5",
    ("yellow", "green", "green", "green"): "GOD_6",
    ("green", "green", "yellow", "yellow"): "MEDIUM_1",
    ("green", "yellow", "green", "yellow"): "MEDIUM_2",
    ("yellow", "green", "green", "yellow"): "MEDIUM_3",
    ("green", "green", "red", "green"): "MEDIUM_4",
    ("green", "red", "green", "green"): "MEDIUM_5",
    ("red", "green", "green", "green"): "MEDIUM_6",
    ("yellow", "yellow", "green", "green"): "MEDIUM_7",
    ("yellow", "green", "yellow", "green"): "MEDIUM_8",
    ("green", "yellow", "yellow", "green"): "MEDIUM_9",
    ("green", "green", "yellow", "red"): "MEDIUM_10",
    ("green", "yellow", "green", "red"): "MEDIUM_11",
    ("yellow", "green", "green", "red"): "MEDIUM_12",
    ("yellow", "yellow", "yellow", "green"): "MEDIUM_13",
    ("yellow", "yellow", "green", "yellow"): "MEDIUM_14",
    ("yellow", "green", "yellow", "yellow"): "MEDIUM_15",
    ("green", "yellow", "yellow", "yellow"): "MEDIUM_16",
    ("yellow", "yellow", "yellow", "yellow"): "MEDIUM_17",
    ("green", "green", "red", "yellow"): "BAD_1",
    ("green", "red", "green", "yellow"): "BAD_2",
    ("red", "green", "green", "yellow"): "BAD_3",
    ("green", "yellow", "red", "green"): "BAD_4",
    ("yellow", "green", "red", "green"): "BAD_5",
    ("yellow", "yellow", "green", "red"): "BAD_6",
    ("yellow", "green", "yellow", "red"): "BAD_7",
    ("green", "yellow", "yellow", "red"): "BAD_8",
    ("green", "red", "yellow", "green"): "BAD_9",
    ("red", "green", "yellow", "green"): "BAD_10",
    ("red", "yellow", "green", "green"): "BAD_11",
    ("yellow", "red", "green", "green"): "BAD_12",
    ("green", "red", "red", "green"): "BAD_13",
    ("red", "green", "red", "green"): "BAD_14",
    ("red", "red", "green", "green"): "BAD_15",
    ("green", "green", "red", "red"): "BAD_16",
    ("green", "red", "green", "red"): "BAD_17",
    ("red", "green", "green", "red"): "BAD_18",
    ("yellow", "yellow", "red", "green"): "BAD_19",
    ("yellow", "red", "yellow", "green"): "BAD_20",
    ("red", "yellow", "yellow", "green"): "BAD_21",
    ("green", "red", "yellow", "red"): "BAD_22",
    ("red", "green", "yellow", "red"): "BAD_23",
    ("red", "yellow", "green", "red"): "BAD_24",
    ("yellow", "red", "green", "red"): "BAD_25",
    ("green", "yellow", "red", "red"): "BAD_26",
    ("yellow", "green", "red", "red"): "BAD_27",
    ("yellow", "red", "red", "green"): "BAD_28",
    ("red", "yellow", "red", "green"): "BAD_29",
    ("red", "red", "yellow", "green"): "BAD_30",
    ("yellow", "yellow", "yellow", "red"): "BAD_31",
    ("yellow", "yellow", "red", "yellow"): "BAD_32",
    ("yellow", "red", "yellow", "yellow"): "BAD_33",
    ("red", "yellow", "yellow", "yellow"): "BAD_34",
    ("green", "red", "red", "yellow"): "BAD_35",
    ("red", "green", "red", "yellow"): "BAD_36",
    ("red", "red", "green", "yellow"): "BAD_37",
    ("yellow", "red", "red", "yellow"): "BAD_38",
    ("red", "yellow", "red", "yellow"): "BAD_39",
    ("red", "red", "yellow", "yellow"): "BAD_40",
    ("green", "red", "red", "red"): "CRISIS_1",
    ("red", "green", "red", "red"): "CRISIS_2",
    ("red", "red", "green", "red"): "CRISIS_3",
    ("yellow", "red", "red", "red"): "CRISIS_4",
    ("red", "yellow", "red", "red"): "CRISIS_5",
    ("red", "red", "yellow", "red"): "CRISIS_6",
    ("yellow", "yellow", "red", "red"): "CRISIS_7",
    ("yellow", "red", "yellow", "red"): "CRISIS_8",
    ("red", "yellow", "yellow", "red"): "CRISIS_9",
    ("red", "red", "red", "green"): "CRISIS_11",
    ("red", "red", "red", "yellow"): "CRISIS_12",
    ("red", "red", "red", "red"): "CRISIS_13",
}

COMBO_DATA = {
    "GOD_1": {"state": "green",
              "comment": "Система в точке идеального равновесия. Все макропоказатели в фазе устойчивого роста."},
    "GOD_2": {"state": "green",
              "comment": "Фиксируем фазу экспансии. Стагнация индекса счастья не является критическим фактором."},
    "GOD_3": {"state": "green",
              "comment": "Несмотря на кризис настроений, фундаментальные показатели подтверждают статус процветания."},
    "GOD_4": {"state": "green",
              "comment": "Незначительное замедление ВВП компенсируется высокой доходностью. Фон благоприятный."},
    "GOD_5": {"state": "green",
              "comment": "Наблюдается торможение темпов роста. Система переходит в фазу инерционного движения."},
    "GOD_6": {"state": "green",
              "comment": "Кризис индекса счастья в сочетании с застоем ВВП требует пересмотра стимулирующей политики."},

    "MEDIUM_1": {"state": "yellow",
                 "comment": "Кризис производства при сохранении доходов переводит систему в режим ожидания."},
    "MEDIUM_2": {"state": "yellow",
                 "comment": "Динамика отсутствует. Эквалайзер фиксирует затяжной период низкой волатильности."},
    "MEDIUM_3": {"state": "yellow",
                 "comment": "Падение индекса счастья на фоне застоя ВВП указывает на системную усталость экономики."},
    "MEDIUM_4": {"state": "yellow",
                 "comment": "Стагнация доходов не препятствует росту. Текущая модель демонстрирует высокую эффективность."},
    "MEDIUM_5": {"state": "yellow",
                 "comment": "Достигнуто плато процветания. Требуется мониторинг для удержания позиций на пике."},
    "MEDIUM_6": {"state": "yellow",
                 "comment": "Отрицательная динамика социального сектора не влияет на общую макроэкономическую устойчивость."},
    "MEDIUM_7": {"state": "yellow",
                 "comment": "Текущие темпы развития признаны недостаточными. Фиксируем стагнацию индикаторов."},
    "MEDIUM_8": {"state": "yellow",
                 "comment": "Ключевые параметры замерли в среднем положении. Драйверы дальнейшего роста не выявлены."},
    "MEDIUM_9": {"state": "yellow",
                 "comment": "Совокупность социального пессимизма и отсутствия роста формирует негативный тренд."},
    "MEDIUM_10": {"state": "yellow",
                  "comment": "Кризис ВВП демпфируется низкой инфляцией, что удерживает систему от рецессии."},
    "MEDIUM_11": {"state": "yellow",
                  "comment": "Фиксируем стабилизацию на низких уровнях. Потенциал для рывка в текущих условиях исчерпан."},
    "MEDIUM_12": {"state": "yellow",
                  "comment": "Температура экономики ниже нормы. Требуется анализ причин депрессивного состояния рынка."},
    "MEDIUM_13": {"state": "yellow",
                  "comment": "Снижение реальных доходов купируется мощным ВВП. Экономика остается в зеленой зоне."},
    "MEDIUM_14": {"state": "yellow",
                  "comment": "Снижение доходов при стагнации ВВП — сигнал к переходу на консервативную модель управления."},
    "MEDIUM_15": {"state": "yellow",
                  "comment": "Система удерживается за счет производства. Социальные индикаторы находятся в зоне риска."},
    "MEDIUM_16": {"state": "yellow",
                  "comment": "Хрупкое равновесие. Экономика балансирует на грани стагнации и перехода к спаду."},
    "MEDIUM_17": {"state": "yellow",
                  "comment": "Полное отсутствие волатильности. Рынок находится в состоянии статистического покоя."},

    "BAD_1": {"state": "red",
              "comment": "Двойной кризис доходов и настроений делает текущую модель крайне неустойчивой."},
    "BAD_2": {"state": "red",
              "comment": "Рецессия ВВП при низкой инфляции. Ситуация требует оперативного вмешательства регулятора."},
    "BAD_3": {"state": "red",
              "comment": "Кризис производства и доходов. Экономический цикл вошел в фазу системного разрушения."},
    "BAD_4": {"state": "red", "comment": "Фиксируем полный технический сбой всех систем. Резервы экономики исчерпаны."},
    "BAD_5": {"state": "red",
              "comment": "Стабилизация инфляции при высоких темпах роста подтверждает прочность текущего курса."},
    "BAD_6": {"state": "red",
              "comment": "Индикаторы подтверждают продолжение цикла роста. Риски на текущий момент минимальны."},
    "BAD_7": {"state": "red",
              "comment": "Отсутствие ценового давления не компенсирует общий упадок социального оптимизма."},
    "BAD_8": {"state": "red",
              "comment": "Синхронное замедление индикаторов. Система вошла в зону долгосрочного застоя."},
    "BAD_9": {"state": "red",
              "comment": "Экономический эквалайзер не фиксирует движения активов. Стагнация подтверждена."},
    "BAD_10": {"state": "red",
               "comment": "Социальный кризис блокирует возможности для восстановления инвестиционной активности."},
    "BAD_11": {"state": "red",
               "comment": "ВВП в глубокой просадке, но накопленный запас доходов удерживает систему от коллапса."},
    "BAD_12": {"state": "red",
               "comment": "Макроэкономические параметры сигнализируют о системном охлаждении всех рынков."},
    "BAD_13": {"state": "red", "comment": "Падение ВВП и кризис индекса счастья подтверждают фазу глубокой депрессии."},
    "BAD_14": {"state": "red",
               "comment": "Застой доходов и цен. Система функционирует в режиме жесткой экономии ресурсов."},
    "BAD_15": {"state": "red",
               "comment": "Фиксируем отсутствие прогресса по ключевым направлениям. Динамика близка к нулевой."},
    "BAD_16": {"state": "red",
               "comment": "Общее снижение показателей при сохранении структуры. Состояние устойчивой стагнации."},
    "BAD_17": {"state": "red",
               "comment": "Остановка роста производства. Система достигла предела текущей технологической модели."},
    "BAD_18": {"state": "red",
               "comment": "Нулевая волатильность цен и объемов. Рынок пребывает в фазе длительного ожидания."},
    "BAD_19": {"state": "red",
               "comment": "Кризис социального самочувствия на фоне застоя лишает систему перспектив развития."},
    "BAD_20": {"state": "red",
               "comment": "Сочетание инфляционного шока и падения производства привело к обвалу рынка."},
    "BAD_21": {"state": "red",
               "comment": "Неконтролируемое снижение макропараметров. Прогноз на следующий квартал негативный."},
    "BAD_22": {"state": "red",
               "comment": "Глубокий кризис. Индикаторы системы находятся за пределами допустимых значений."},
    "BAD_23": {"state": "red",
               "comment": "Кризис реальных доходов населения — основной сдерживающий фактор для растущего ВВП."},
    "BAD_24": {"state": "red",
               "comment": "Ухудшение показателей доходов переводит экономику в режим отрицательной стагнации."},
    "BAD_25": {"state": "red",
               "comment": "Инфляционное давление при падении доходов формирует критически негативный фон."},
    "BAD_26": {"state": "red",
               "comment": "Индикаторы системы демонстрируют нисходящий тренд. Застой переходит в фазу спада."},
    "BAD_27": {"state": "red",
               "comment": "Фиксируем остановку экономических циклов. Рост в текущих условиях не прогнозируется."},
    "BAD_28": {"state": "red",
               "comment": "Отрицательная динамика доходов и ВВП привела к развитию масштабной рецессии."},
    "BAD_29": {"state": "red",
               "comment": "Инфляционный взрыв при парализованном производстве. Экономика в критическом состоянии."},
    "BAD_30": {"state": "red",
               "comment": "Наблюдается деградация рыночных механизмов. Требуются экстренные меры реанимации."},
    "BAD_31": {"state": "red",
               "comment": "Полное отсутствие внутренних ресурсов для восстановления. Системный коллапс."},
    "BAD_32": {"state": "red",
               "comment": "Переход инфляции в зону риска начинает разрушать общую стабильность системы."},
    "BAD_33": {"state": "red",
               "comment": "Рост цен провоцирует охлаждение спроса. Система находится в состоянии нестабильности."},
    "BAD_34": {"state": "red",
               "comment": "Высокая инфляция привела к социальному кризису. Требуется корректировка курса ДКП."},
    "BAD_35": {"state": "red",
               "comment": "Инфляционный шок замедлил темпы ВВП. Прогнозируем переход к затяжной стагнации."},
    "BAD_36": {"state": "red",
               "comment": "Стагфляционные процессы: цены растут при полном отсутствии экономического развития."},
    "BAD_37": {"state": "red",
               "comment": "Совокупный кризис настроений и инфляции. Покупательная способность под угрозой."},
    "BAD_38": {"state": "red",
               "comment": "Ценовой кризис обрушил реальный сектор экономики. Рецессия официально зафиксирована."},
    "BAD_39": {"state": "red", "comment": "Стагфляционная ловушка в терминальной стадии. Капитал покидает систему."},
    "BAD_40": {"state": "red",
               "comment": "Максимальный уровень рыночного риска. Система утратила внутреннюю устойчивость."},

    "CRISIS_1": {"state": "red",
                 "comment": "Рост ВВП полностью нивелируется агрессивной инфляцией. Чистый эффект — нулевой."},
    "CRISIS_2": {"state": "red",
                 "comment": "Рост цен при застое доходов населения. Наблюдается снижение качества жизни."},
    "CRISIS_3": {"state": "red", "comment": "Эрозия капитала из-за инфляции на фоне глубокого социального пессимизма."},
    "CRISIS_4": {"state": "red",
                 "comment": "Ценовое давление при стагнации производства ставит под вопрос устойчивость рынка."},
    "CRISIS_5": {"state": "red",
                 "comment": "Совокупность высокой инфляции и стагнации ВВП спровоцировала резкий спад."},
    "CRISIS_6": {"state": "red",
                 "comment": "Фиксируем фазу глубокой рецессии. Социальные и экономические потери неизбежны."},
    "CRISIS_7": {"state": "red",
                 "comment": "Резкое ухудшение фундаментальных показателей. Состояние системы признано критическим."},
    "CRISIS_8": {"state": "red",
                 "comment": "Девальвация достижений прошлого периода. Экономика в точке исторического минимума."},
    "CRISIS_9": {"state": "red",
                 "comment": "Тотальное разрушение стабильности. Процесс восстановления будет длительным."},
    "CRISIS_11": {"state": "red",
                  "comment": "Сочетание инфляционного и доходного кризисов удерживает рынок в депрессии."},
    "CRISIS_12": {"state": "red",
                  "comment": "Ухудшение условий ведения бизнеса и падение уровня жизни. Система деградирует."},
    "CRISIS_13": {"state": "red",
                  "comment": "Параметры находятся на критических отметках. Риск перехода в депрессию максимален."},
}


def calculate_economy(rate, money_supply, operations, subsidies):
    base_inflation = 7.0
    base_income = 90.0
    base_gdp = 97.5
    base_happiness = 55.0

    inflation_from_rate = -rate * 0.12
    income_from_rate = -rate * 0.25
    gdp_from_rate = -rate * 0.20
    happiness_from_rate = -rate * 0.18

    inflation_from_money = money_supply * 0.15
    income_from_money = money_supply * 0.20
    gdp_from_money = money_supply * 0.22
    happiness_from_money = money_supply * 0.12

    inflation_from_ops = operations * 0.08
    income_from_ops = operations * 0.18
    gdp_from_ops = operations * 0.18
    happiness_from_ops = operations * 0.22

    inflation_from_subsidies = subsidies * 0.10
    income_from_subsidies = subsidies * 0.28
    gdp_from_subsidies = subsidies * 0.18
    happiness_from_subsidies = subsidies * 0.25

    inflation = base_inflation + inflation_from_rate + inflation_from_money + inflation_from_ops + inflation_from_subsidies
    inflation = max(0, min(30, inflation))

    real_income = base_income + income_from_rate + income_from_money + income_from_ops + income_from_subsidies
    real_income = max(50, min(150, real_income))

    current_gdp = base_gdp + gdp_from_rate + gdp_from_money + gdp_from_ops + gdp_from_subsidies
    current_gdp = max(60, min(140, current_gdp))

    happiness = base_happiness + happiness_from_rate + happiness_from_money + happiness_from_ops + happiness_from_subsidies
    happiness = max(20, min(100, happiness))

    gdp_change = ((current_gdp - 100) / 100) * 100

    def get_inflation_state(inflation_value):
        if inflation_value <= 4:
            return "green"
        elif inflation_value > 10:
            return "red"
        return "yellow"

    def get_income_state(income_value):
        if income_value >= 100:
            return "green"
        elif income_value >= 80:
            return "yellow"
        return "red"

    def get_gdp_state(gdp_change_value):
        if gdp_change_value >= 0:
            return "green"
        elif gdp_change_value >= -5:
            return "yellow"
        return "red"

    def get_happiness_state(happiness_value):
        if happiness_value >= 70:
            return "green"
        elif happiness_value >= 40:
            return "yellow"
        return "red"

    states = {
        "inflation": get_inflation_state(inflation),
        "income": get_income_state(real_income),
        "gdp": get_gdp_state(gdp_change),
        "happiness": get_happiness_state(happiness)
    }

    key = (states["inflation"], states["income"], states["gdp"], states["happiness"])
    combo_id = COMBO_IDS.get(key, "MEDIUM_1")
    combo_info = COMBO_DATA.get(combo_id, {"state": "yellow", "comment": "Ситуация неопределенная. Мур?"})

    overall_state = combo_info["state"]

    if overall_state == "green":
        overall_text = "Процветание"
    elif overall_state == "yellow":
        overall_text = "Стагнация"
    else:
        overall_text = "Кризис"

    state_to_score = {"green": 100, "yellow": 50, "red": 0}

    overall_score = (
        state_to_score[states["inflation"]] * 0.25 +
        state_to_score[states["income"]] * 0.25 +
        state_to_score[states["gdp"]] * 0.25 +
        state_to_score[states["happiness"]] * 0.25
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
        "overall_comment": combo_info["comment"],
        "combo_id": combo_id
    }


@app.route('/')
def index():
    return render_template('index.html')


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
    print("Выбран символ:", data)
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
