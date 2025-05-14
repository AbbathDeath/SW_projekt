import inputs
from gpiozero import Motor
import time

left_motor = Motor(forward=12, backward=13)
right_motor = Motor(forward=18, backward=19)

def get_gamepad_input():
    try:
        events = inputs.get_gamepad()
        for event in events:
            if event.ev_type == "Absolute":
                if event.code == "ABS_Y":  # Левый стик (вперёд/назад)
                    throttle = (event.state - 32768) / 32768  # [-1, 1]
                    return throttle, None
                elif event.code == "ABS_X":  # Левый стик (влево/вправо)
                    steering = (event.state - 32768) / 32768  # [-1, 1]
                    return None, steering
    except:
        return None, None

try:
    while True:
        throttle, steering = get_gamepad_input()
        
        if throttle is not None:
            # Преобразуем throttle в скорость моторов (0...1)
            speed = abs(throttle) * 0.5  # Ограничиваем скорость
            
            if throttle > 0.1:  # Вперёд
                left_motor.forward(speed)
                right_motor.forward(speed)
            elif throttle < -0.1:  # Назад
                left_motor.backward(speed)
                right_motor.backward(speed)
            else:  # Стоп
                left_motor.stop()
                right_motor.stop()
        
        if steering is not None:
            # Поворот (чем больше отклонение стика, тем резче поворот)
            if steering < -0.3:  # Влево
                left_motor.backward(0.3)
                right_motor.forward(0.5)
            elif steering > 0.3:  # Вправо
                left_motor.forward(0.5)
                right_motor.backward(0.3)
        
        time.sleep(0.01)

except KeyboardInterrupt:
    left_motor.stop()
    right_motor.stop()
