from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update', methods=['POST'])
def update():
    data = request.json
    print("Получены значения:", data)
    return jsonify({"status": "ok"})

@app.route('/select-symbol', methods=['POST'])
def select_symbol():
    data = request.json
    print("Выбран символ:", data)
    return jsonify({"status": "ok"})

@app.route('/get-color', methods=['POST'])
def get_color():
    data = request.json
    values = data.get('values', [])

    if values:
        avg = sum(values) / len(values)
    else:
        avg = 0

    # Условия для цвета по среднему значению
    if avg < -60:
        color = '#e74c3c'  # красный
    elif avg < -20:
        color = '#f39c12'  # оранжевый
    elif avg < 20:
        color = '#f1c40f'  # желтый
    elif avg < 60:
        color = '#2ecc71'  # зеленый
    else:
        color = '#3498db'  # синий

    return jsonify({'color': color})


@app.route('/get-bg-color', methods=['POST'])
def get_bg_color():
    data = request.json
    symbol_color = data.get('color', '#e74c3c')

    return jsonify({'bg_color': symbol_color})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)