from flask import Flask, render_template
from gpiozero import Motor
import time

control_app = Flask(__name__)

motor1 = Motor(forward=23, backward=24)  
motor2 = Motor(forward=27, backward=22)  

def motor_forward():
    motor1.forward()
    motor2.forward()

def motor_stop():
    motor1.stop()
    motor2.stop()

def motor_backward():
    motor1.backward()
    motor2.backward()

def motor_left():
    motor1.forward()
    motor2.backward()

def motor_right():
    motor1.backward()
    motor2.forward()


@control_app.route('/')
def index():
    return render_template('index.html')

@control_app.route('/forward')
def forward():
    motor_forward()
    return "Moving Forward"

@control_app.route('/backward')
def backward():
    motor_backward()
    return "Moving Backward"

@control_app.route('/left')
def left():
    motor_left()
    return "Turning left"

@control_app.route('/right')
def right():
    motor_right()
    return "Turning right"

@control_app.route('/stop')
def stop():
    motor_stop()
    return "Stop"

if __name__ == '__main__':
    try:
        control_app.run(host='0.0.0.0', port=5000)
    finally:
        motor1.stop()
        motor2.stop()
