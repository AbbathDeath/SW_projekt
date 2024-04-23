from flask import Flask, render_template
import Rpi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

in1 = 29
in2 = 31
in3 = 37
in4 = 35

GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)



app = Flask(__name__, template_folder='C:\\Users\\Abbath\\Documents\\Projects\\rpi')


@app.route('/')

def index():
    return render_template('index.html')
@app.route('/forward', methods=['POST'])
def move_forward():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)

@app.route('/left', methods=['POST'])
def turn_left():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)

@app.route('/stop', methods=['POST'])
def stop():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)

@app.route('/right', methods=['POST'])
def turn_right():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)

@app.route('/back', methods=['POST'])
def move_backward():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)

if __name__ == '__main__':
    app.run(debug=True) 
