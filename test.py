import curses
from gpiozero import Motor
from time import sleep

class Vehicle:
    def __init__(self):
        # Инициализация моторов с поддержкой PWM через gpiozero
        self.left_motor = Motor(forward=12, backward=13, pwm=True)
        self.right_motor = Motor(forward=18, backward=19, pwm=True)
        self.speed = 0.5  # Начальная скорость (0-1)

    def forward(self):
        self.left_motor.forward(self.speed)
        self.right_motor.forward(self.speed)

    def backward(self):
        self.left_motor.backward(self.speed)
        self.right_motor.backward(self.speed)

    def left(self):
        self.left_motor.backward(self.speed*0.5)  # Левый мотор медленно назад
        self.right_motor.forward(self.speed)      # Правый мотор вперед

    def right(self):
        self.left_motor.forward(self.speed)      # Левый мотор вперед
        self.right_motor.backward(self.speed*0.5) # Правый мотор медленно назад

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()

    def increase_speed(self):
        self.speed = min(1.0, self.speed + 0.1)

    def decrease_speed(self):
        self.speed = max(0.1, self.speed - 0.1)

    def map_key_to_command(self, key):
        map = {
            curses.KEY_UP: self.forward,
            curses.KEY_DOWN: self.backward,
            curses.KEY_LEFT: self.left,
            curses.KEY_RIGHT: self.right,
            ord('+'): self.increase_speed,
            ord('='): self.increase_speed,
            ord('-'): self.decrease_speed,
            ord(' '): self.stop
        }
        return map.get(key)

    def control(self, key):
        return self.map_key_to_command(key)


def main(window):
    rpi_vehicle = Vehicle()
    window.nodelay(True)  # Неблокирующий ввод
    curses.curs_set(0)    # Скрыть курсор
    
    try:
        while True:
            key = window.getch()
            
            if key == -1:
                continue  # Клавиша не нажата
                
            action = rpi_vehicle.control(key)
            if action:
                action()
                
            sleep(0.05)  # Небольшая задержка
            
    except KeyboardInterrupt:
        pass
    finally:
        rpi_vehicle.stop()


if __name__ == "__main__":
    curses.wrapper(main)
