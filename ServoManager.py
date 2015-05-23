
import logging
from RPIO import PWM

class Servo:
    """
    Represent a servo motor
    """

    def __init__(self, gpio):
        self.logger = logging.getLogger('Servo')
        self.logger.debug('__init__')
        self.servo = PWM.Servo(pulse_incr_us=1)
        self.gpio = gpio
        self.frequency = 50 # 50hz frequency
        self.angle_moins_90 = 250 # 250 us
        self.angle_90 = 2300 # 2300us

    def get_duty_cycle(self, angle):
        angle += 90
        return angle * self.angle_90 / 90

    def move(self, angle):
        self.logger.debug('Servo %d : angle : %d' % (self.gpio, angle))
        if angle <= -90:
            angle = -89
            self.logger.debug('angle to low, set to -89')
        elif angle > 90:
            angle = 90
            self.logger.debug('angle to high, set to 90')
        self.set_dutycycle(self.get_duty_cycle(angle))

    def set_dutycycle(self, dutycyle):
        self.logger.debug('Servo %d : duty_cycle : %d' % (self.gpio, dutycyle))
        self.servo.set_servo(self.gpio, dutycyle)

class ServoManager:
    """
    Used to manage the servos with GPIOs
    """

    __shared_state = {}

    def __init__(self, gpio_up_down=None, gpio_right_left=None):
        self.__dict__ = self.__shared_state
        if gpio_up_down is not None and gpio_right_left is not None:
            self.servo_up_down = Servo(gpio=gpio_up_down)
            self.servo_right_left = Servo(gpio=gpio_right_left)

    def move_up_down(self, angle):
        self.servo_up_down.move(angle)

    def move_right_left(self, angle):
        self.servo_right_left.move(angle)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')
    servo = Servo(2)
    while True:
        servo.move(input())
