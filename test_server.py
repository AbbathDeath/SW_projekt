from flask import Flask, render_template

app = Flask(__name__, template_folder='C:\\Users\\Abbath\\Documents\\Projects\\rpi')

# Define route for the root URL
@app.route('/')

def index():
    # Render your HTML template
    return render_template('index.html')
# Обработчики маршрутов для каждого направления движения
@app.route('/forward', methods=['POST'])
def move_forward():
    # Здесь выполняется код для движения машинки вперед
    return 'Moving forward'

@app.route('/left', methods=['POST'])
def turn_left():
    # Здесь выполняется код для поворота машинки влево
    return 'Turning left'

@app.route('/stop', methods=['POST'])
def stop():
    # Здесь выполняется код для остановки машинки
    return 'Stopping'

@app.route('/right', methods=['POST'])
def turn_right():
    # Здесь выполняется код для поворота машинки вправо
    return 'Turning right'

@app.route('/back', methods=['POST'])
def move_backward():
    # Здесь выполняется код для движения машинки назад
    return 'Moving backward'

if __name__ == '__main__':
    app.run(debug=True) # Запуск сервера в режиме отладки
