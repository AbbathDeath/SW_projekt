import curses
import time
import inputs  # Для геймпада
from gpiozero import Motor

class Vehicle:
    def __init__(self):
        self.left_motor = Motor(forward=12, backward=13, pwm=True)
        self.right_motor = Motor(forward=18, backward=19, pwm=True)
        
        # Настройки калибровки
        self.base_speed = 0.5
        self.cumulative_error = 0.0  # Накопленная ошибка увода
        self.correction_step = 0.01  # Шаг коррекции (подбирается)
        self.last_correction_time = time.time()
        
        # Для геймпада
        self.gamepad_connected = False
        try:
            self.gamepad = inputs.devices.gamepads[0]
            self.gamepad_connected = True
        except:
            print("Геймпад не найден, используется клавиатура")

    def set_motors(self, left_speed, right_speed):
        """Установка скорости с ограничением"""
        self.left_motor.value = max(-1, min(1, left_speed))
        self.right_motor.value = max(-1, min(1, right_speed))

    def forward(self):
        # Автокоррекция увода
        time_elapsed = time.time() - self.last_correction_time
        if time_elapsed > 1.0:  # Корректируем каждую секунду
            self.cumulative_error += self.correction_step * time_elapsed
            self.last_correction_time = time.time()
        
        left_speed = self.base_speed - self.cumulative_error
        right_speed = self.base_speed + self.cumulative_error
        self.set_motors(left_speed, right_speed)

    def backward(self):
        self.set_motors(-self.base_speed, -self.base_speed)

    def left(self):
        self.set_motors(-self.base_speed*0.3, self.base_speed)

    def right(self):
        self.set_motors(self.base_speed, -self.base_speed*0.3)

    def stop(self):
        self.set_motors(0, 0)
        self.cumulative_error = 0.0  # Сброс ошибки при остановке

    def get_gamepad_input(self):
        """Чтение данных с геймпада"""
        if not self.gamepad_connected:
            return None
            
        try:
            events = inputs.get_gamepad()
            for event in events:
                if event.code == "ABS_Y":  # Левый стик (вперёд/назад)
                    return ("throttle", (event.state - 32768) / 32768)
                elif event.code == "ABS_X":  # Левый стик (влево/вправо)
                    return ("steering", (event.state - 32768) / 32768)
        except:
            return None

    def map_key_to_command(self, key):
        """Совмещаем управление клавиатурой и геймпадом"""
        # Сначала проверяем геймпад
        gamepad_input = self.get_gamepad_input()
        if gamepad_input:
            input_type, value = gamepad_input
            if input_type == "throttle":
                return self.forward if value < -0.5 else self.backward if value > 0.5 else self.stop
            elif input_type == "steering":
                return self.left if value < -0.3 else self.right if value > 0.3 else None
        
        # Если геймпада нет, используем клавиатуру
        return {
            curses.KEY_UP: self.forward,
            curses.KEY_DOWN: self.backward,
            curses.KEY_LEFT: self.left,
            curses.KEY_RIGHT: self.right,
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