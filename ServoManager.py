
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
        self.angle_0 = 250 # 250 us
        self.angle_180 = 2300 # 2300us

    def get_duty_cycle(self, angle):
        return (angle * self.angle_180) / 180

    def move(self, angle):
        duty_cycle = self.get_duty_cycle(angle)
        self.logger.debug('Servo %d : angle : %d, duty_cycle : %d' % (self.gpio, angle, duty_cycle))
        self.servo.set_servo(self.gpio, duty_cycle)


class ServoManager:
    """
    Used to manage the servos with GPIOs
    """

    instance = None

    def __new__(cls, *args, **kwargs):
        """
        because it's a singleton
        """
        if cls.instance is None:
            cls.instance = object.__new__(cls)
        return cls.instance

    def __init__(self):
        self.servo_up_down = Servo()
        self.servo_right_left = Servo()

    def move_up_down(self, angle):
        self.servo_up_down.move(angle)

    def move_right_lef(self, angle):
        self.servo_right_left.move(angle)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')
    servo = Servo(17)
    while True:
        servo.move(input())
