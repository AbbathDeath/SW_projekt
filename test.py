import curses
from gpiozero import Motor
from time import sleep

class Vehicle:
    def __init__(self):
        self.left_motor = Motor(forward=13, backward=12, pwm=True)
        self.right_motor = Motor(forward=19, backward=18, pwm=True)
        self.speed = 0.5  # Начальная скорость (0-1)
        
    def forward(self):
        self.left_motor.forward(self.speed)
        self.right_motor.forward(self.speed)

    def backward(self):
        self.left_motor.backward(self.speed)
        self.right_motor.backward(self.speed)

    def left(self):
        self.right_motor.forward(self.speed)
        self.left_motor.backward(self.speed*0.3)

    def right(self):
        self.left_motor.forward(self.speed)
        self.right_motor.backward(self.speed*0.3)

    def increase_speed(self):
        self.speed = min(1.0, round(self.speed + 0.1, 1))
        print(f"Speed increased to: {self.speed}")

    def decrease_speed(self):
        self.speed = max(0.1, round(self.speed - 0.1, 1))
        print(f"Speed decreased to: {self.speed}")

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
