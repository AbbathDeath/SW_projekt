import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

m1a = 32
m1b = 31
m2a = 36
m2b = 35


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


motor_forward()
time.sleep(2)
motor_stop()
time.sleep(2)
motor_backward()
time.sleep(2)
motor_stop()
