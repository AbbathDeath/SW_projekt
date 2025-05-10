import lgpio
import time

# Open GPIO chip
h = lgpio.gpiochip_open(0)

# Define GPIO pins (BCM numbering)
m1a = 23  # BCM GPIO 23
m1b = 24  # BCM GPIO 24
m2a = 27  # BCM GPIO 27
m2b = 22  # BCM GPIO 22

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

# Motor control functions
def motor_forward():
    print("Moving Forward")
    lgpio.gpio_write(h, m1a, 1)
    lgpio.gpio_write(h, m1b, 0)
    lgpio.gpio_write(h, m2a, 1)
    lgpio.gpio_write(h, m2b, 0)

def motor_stop():
    print("Stopping")
    lgpio.gpio_write(h, m1a, 0)
    lgpio.gpio_write(h, m1b, 0)
    lgpio.gpio_write(h, m2a, 0)
    lgpio.gpio_write(h, m2b, 0)

def motor_backward():
    print("Moving Backward")
    lgpio.gpio_write(h, m1a, 0)
    lgpio.gpio_write(h, m1b, 1)
    lgpio.gpio_write(h, m2a, 0)
    lgpio.gpio_write(h, m2b, 1)

def motor_left():
    print("Turning Left")
    lgpio.gpio_write(h, m1a, 1)
    lgpio.gpio_write(h, m1b, 0)
    lgpio.gpio_write(h, m2a, 0)
    lgpio.gpio_write(h, m2b, 1)

def motor_right():
    print("Turning Right")
    lgpio.gpio_write(h, m1a, 0)
    lgpio.gpio_write(h, m1b, 1)
    lgpio.gpio_write(h, m2a, 1)
    lgpio.gpio_write(h, m2b, 0)

try:
    # Simple test sequence
    print("Starting motor test sequence...")
    
    motor_forward()
    time.sleep(2)
    
    motor_stop()
    time.sleep(1)
    
    motor_backward()
    time.sleep(2)
    
    motor_stop()
    time.sleep(1)
    
    motor_left()
    time.sleep(2)
    
    motor_stop()
    time.sleep(1)
    
    motor_right()
    time.sleep(2)
    
    motor_stop()
    
    print("Test sequence completed!")

except KeyboardInterrupt:
    print("\nProgram stopped by user")
finally:
    # Clean up
    motor_stop()
    lgpio.gpiochip_close(h)
    print("GPIO resources released")
