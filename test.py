import curses
from gpiozero import Motor
from time import sleep

class Vehicle:
    def __init__(self):
        self.left_motor = Motor(forward=12, backward=13, pwm=True)
        self.right_motor = Motor(forward=18, backward=19, pwm=True)
        self.left_speed_correction = 1.0   
        self.right_speed_correction = 1.0  
        correction_per_second = 0.03
        
        self.base_speed = 0.5 
    def set_motors(self, left_speed, right_speed):
        self.left_motor.value = left_speed * self.left_speed_correction
        self.right_motor.value = right_speed * self.right_speed_correction

    def forward(self):
        left_speed = self.base_speed - (correction_per_second * time_elapsed)
        self.set_motors(left_speed, self.base_speed)


    def backward(self):
        self.set_motors(-self.base_speed, -self.base_speed)

    def left(self):
        self.set_motors(-self.base_speed*0.3, self.base_speed)

    def right(self):
        self.set_motors(self.base_speed, -self.base_speed*0.3)

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()

    def map_key_to_command(self, key):
        return {
            curses.KEY_UP: self.forward,
            curses.KEY_DOWN: self.backward,
            curses.KEY_LEFT: self.left,
            curses.KEY_RIGHT: self.right,
            ord('+'): self.increase_speed,
            ord('='): self.increase_speed,
            ord('-'): self.decrease_speed
        }.get(key)

    def control(self, key):
        return self.map_key_to_command(key)


rpi_vehicle = Vehicle()


def main(window):
    next_key = None

    while True:
        curses.halfdelay(1)
        if next_key is None:
            key = window.getch()
            print(key)
        else:
            key = next_key
            next_key = None
        if key != -1:
            # KEY PRESSED
            curses.halfdelay(1)
            action = rpi_vehicle.control(key)
            if action:
                action()
            next_key = key
            while next_key == key:
                next_key = window.getch()
            # KEY RELEASED
            rpi_vehicle.left_motor.stop()
            rpi_vehicle.right_motor.stop()


if __name__ == "__main__":
    curses.wrapper(main)
