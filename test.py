import curses
import time
import math
from gpiozero import Motor

class Vehicle:
    def __init__(self):
        self.left_motor = Motor(forward=12, backward=13, pwm=True)
        self.right_motor = Motor(forward=18, backward=19, pwm=True)
        
        # Настройки плавности
        self.base_speed = 0.5  # Базовая скорость (0-1)
        self.max_steering = 0.8  # Максимальный угол поворота
        self.steering_smoothness = 0.2  # Коэф. плавности (0.1-0.5)
        self.last_steering = 0  # Для плавного изменения

    def set_motors(self, left_speed, right_speed):
        """Установка скорости с плавным изменением"""
        # Плавный переход от текущей скорости к целевой
        current_left = self.left_motor.value
        current_right = self.right_motor.value
        
        smooth_left = current_left + (left_speed - current_left) * self.steering_smoothness
        smooth_right = current_right + (right_speed - current_right) * self.steering_smoothness
        
        self.left_motor.value = max(-1, min(1, smooth_left))
        self.right_motor.value = max(-1, min(1, smooth_right))

    def forward(self, steering=0):
        """Движение вперед с плавным поворотом"""
        # Ограничиваем steering [-1, 1] и применяем квадратичную кривую
        steering = max(-1, min(1, steering))
        steering = math.copysign(steering ** 2, steering)  # Квадратичное смягчение
        
        # Рассчитываем скорости для каждого мотора
        left_speed = self.base_speed * (1 - steering)
        right_speed = self.base_speed * (1 + steering)
        
        self.set_motors(left_speed, right_speed)

    def backward(self):
        self.set_motors(-self.base_speed, -self.base_speed)

    def stop(self):
        self.set_motors(0, 0)

    def map_key_to_command(self, key):
        """Обработка клавиш с плавным управлением"""
        return {
            curses.KEY_UP: lambda: self.forward(0),  # Прямо
            curses.KEY_DOWN: self.backward,
            curses.KEY_LEFT: lambda: self.forward(-0.5),  # Плавный левый поворот
            curses.KEY_RIGHT: lambda: self.forward(0.5),  # Плавный правый поворот
            ord(' '): self.stop
        }.get(key)

    def control(self, key):
        return self.map_key_to_command(key)


def main(window):
    rpi_vehicle = Vehicle()
    next_key = None

    while True:
        curses.halfdelay(1)
        if next_key is None:
            key = window.getch()
        else:
            key = next_key
            next_key = None

        if key != -1:
            action = rpi_vehicle.control(key)
            if action:
                action()
            next_key = key
            while next_key == key:
                next_key = window.getch()
            rpi_vehicle.stop()


if __name__ == "__main__":
    curses.wrapper(main)
