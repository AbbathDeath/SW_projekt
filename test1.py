from flask import Flask, render_template
import RPi.GPIO as GPIO
import time

control_app = Flask(__name__)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

m1a = 23 #bialy23
m1b = 24 #zolty24
m2a = 27 #zielony27
m2b = 22 #fielotowy22


GPIO.setup(m1a, GPIO.OUT)
GPIO.setup(m1b, GPIO.OUT)
GPIO.setup(m2a, GPIO.OUT)
GPIO.setup(m2b, GPIO.OUT)

def motor_forward():
    GPIO.output(m1a, GPIO.HIGH)
    GPIO.output(m1b, GPIO.LOW)
    GPIO.output(m2a, GPIO.HIGH)
    GPIO.output(m2b, GPIO.LOW)

def motor_stop():
    GPIO.output(m1a, GPIO.LOW)
    GPIO.output(m1b, GPIO.LOW)
    GPIO.output(m2a, GPIO.LOW)
    GPIO.output(m2b, GPIO.LOW)

def motor_backward():
    GPIO.output(m1a, GPIO.LOW)
    GPIO.output(m1b, GPIO.HIGH)
    GPIO.output(m2a, GPIO.LOW)
    GPIO.output(m2b, GPIO.HIGH)

def motor_left():
    GPIO.output(m1a, GPIO.HIGH)
    GPIO.output(m1b, GPIO.LOW)
    GPIO.output(m2a, GPIO.LOW)
    GPIO.output(m2b, GPIO.HIGH)

def motor_right():
    GPIO.output(m1a, GPIO.LOW)
    GPIO.output(m1b, GPIO.HIGH)
    GPIO.output(m2a, GPIO.HIGH)
    GPIO.output(m2b, GPIO.LOW)



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
    control_app(host = '0.0.0.0', port = 5000)
