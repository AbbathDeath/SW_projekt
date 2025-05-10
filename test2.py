import lgpio
import time

# Open GPIO chip
h = lgpio.gpiochip_open(0)

# Define GPIO pins (BCM numbering)
m1a = 23  # Left motor forward
m1b = 24  # Left motor backward
m2a = 27  # Right motor forward
m2b = 22  # Right motor backward

# Setup pins as outputs
lgpio.gpio_claim_output(h, m1a)
lgpio.gpio_claim_output(h, m1b)
lgpio.gpio_claim_output(h, m2a)
lgpio.gpio_claim_output(h, m2b)

# Initialize all pins to LOW
lgpio.gpio_write(h, m1a, 0)
lgpio.gpio_write(h, m1b, 0)
lgpio.gpio_write(h, m2a, 0)
lgpio.gpio_write(h, m2b, 0)

# Individual motor control functions
def left_motor_forward():
    lgpio.gpio_write(h, m1a, 1)
    lgpio.gpio_write(h, m1b, 0)
    
def left_motor_backward():
    lgpio.gpio_write(h, m1a, 0)
    lgpio.gpio_write(h, m1b, 1)
    
def right_motor_forward():
    lgpio.gpio_write(h, m2a, 1)
    lgpio.gpio_write(h, m2b, 0)
    
def right_motor_backward():
    lgpio.gpio_write(h, m2a, 0)
    lgpio.gpio_write(h, m2b, 1)
    
def all_motors_stop():
    lgpio.gpio_write(h, m1a, 0)
    lgpio.gpio_write(h, m1b, 0)
    lgpio.gpio_write(h, m2a, 0)
    lgpio.gpio_write(h, m2b, 0)

# Combined movement functions
def motor_forward():
    left_motor_forward()
    right_motor_forward()

def motor_backward():
    left_motor_backward()
    right_motor_backward()

def motor_left():
    left_motor_backward()  # Reverse left motor
    right_motor_forward()  # Forward right motor

def motor_right():
    left_motor_forward()   # Forward left motor
    right_motor_backward() # Reverse right motor

print("Robot Motor Diagnostic")
print("---------------------")
print("1 - Test left motor forward")
print("2 - Test left motor backward")
print("3 - Test right motor forward")
print("4 - Test right motor backward")
print("---------------------")
print("w - Both motors forward")
print("s - Both motors backward")
print("a - Turn left")
print("d - Turn right")
print("x - Stop all motors")
print("q - Quit")
print("---------------------")

try:
    while True:
        command = input("Enter command: ")
        
        if command == '1':
            print("Left motor forward")
            left_motor_forward()
            right_motor_stop = lambda: lgpio.gpio_write(h, m2a, 0) and lgpio.gpio_write(h, m2b, 0)
            right_motor_stop()
        elif command == '2':
            print("Left motor backward")
            left_motor_backward()
            right_motor_stop = lambda: lgpio.gpio_write(h, m2a, 0) and lgpio.gpio_write(h, m2b, 0)
            right_motor_stop()
        elif command == '3':
            print("Right motor forward")
            right_motor_forward()
            left_motor_stop = lambda: lgpio.gpio_write(h, m1a, 0) and lgpio.gpio_write(h, m1b, 0)
            left_motor_stop()
        elif command == '4':
            print("Right motor backward")
            right_motor_backward()
            left_motor_stop = lambda: lgpio.gpio_write(h, m1a, 0) and lgpio.gpio_write(h, m1b, 0)
            left_motor_stop()
        elif command.lower() == 'w':
            print("Both motors forward")
            motor_forward()
        elif command.lower() == 's':
            print("Both motors backward")
            motor_backward()
        elif command.lower() == 'a':
            print("Turning Left")
            motor_left()
        elif command.lower() == 'd':
            print("Turning Right")
            motor_right()
        elif command.lower() == 'x':
            print("Stopping all motors")
            all_motors_stop()
        elif command.lower() == 'q':
            print("Quitting")
            break
        else:
            print("Unknown command")

except KeyboardInterrupt:
    print("\nProgram stopped by user")
finally:
    # Clean up
    all_motors_stop()
    lgpio.gpiochip_close(h)
    print("GPIO resources released")
