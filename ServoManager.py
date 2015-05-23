
import logging
from RPIO import PWM

class Servo:
    """
    Represent a servo motor
    """

    def __init__(self, gpio, dma):
        self.logger = logging.getLogger('Servo')
        self.logger.debug('__init__')
        self.servo = PWM.Servo(dma_channel=dma, pulse_incr_us=1)
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

    __shared_state = {}

    def __init__(self, gpios=None):
        self.__dict__ = self.__shared_state
        if gpios is not None:
            self.servo_up_down = Servo(dma=gpios[0][0],gpio=gpios[0][1])
            self.servo_right_left = Servo(dma=gpios[1][0],gpio=gpios[1][1])

    def move_up_down(self, angle):
        self.servo_up_down.move(angle)

    def move_right_left(self, angle):
        self.servo_right_left.move(angle)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')
    servo = Servo(2, 0)
    while True:
        servo.move(input())
