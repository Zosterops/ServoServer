
class Servo:
    """
    Represent a servo motor
    """

    def __init__(self, gpio):
        self.gpio = gpio
        self.frequency = 50 # 50hz frequency
        self.angle_0 = 5 # 0.5 ms
        self.angle_180 = 25 # 2.5ms

    def get_duty_cycle(self, angle):
        return 5

    def move(self, angle):
        pass


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

