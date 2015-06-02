
import json
import logging
from struct import unpack
import SocketServer
from ServoManager import ServoManager

class ServoServerHandler(SocketServer.BaseRequestHandler):
    """
    ServoServerHandler handle every requests made by the user
    """

    def __init__(self, request, client_address, server):
        """
        Construct a new 'ServoServerHandler' object
        """
        self.logger = logging.getLogger('ServoServerHandler')
        self.logger.debug('__init__')
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def get_cmd_json(self):
        """
        First reads the size of the data
        Then reads the data of size size
        """
        data = ""
        size = self.request.recv(2)
        if len(size) == 2:
            size = unpack('>H', size)[0]
            data = self.request.recv(size)
        return data

    def exec_cmd(self, cmd):
        """
        execute the cmd
        """
        if cmd.has_key('type') and cmd['type'] == "movement":
            if cmd.has_key('x') and cmd.has_key('y'):
                x = int(cmd['x'])
                y = int(cmd['y'])
                servo_manager = ServoManager()
                servo_manager.move_up_down(x)
                servo_manager.move_right_left(y)
            else:
                self.logger.debug('Movement packet doesn\'t have x and y values')
        else:
            self.logger.debug('Unknown packet : %s' % repr(cmd))

    def setup(self):
        self.logger.debug('setup')

    def handle(self):
        """
        Handle every request made by the users
        Simply call get_cmd_json() and parse it with json.loads()
        """
        self.logger.debug('handle')
        while True:
            data = self.get_cmd_json()
            self.logger.debug('json raw data : %s' % repr(data))

            try:
                cmd = json.loads(data)
                self.logger.debug('json : %s' % repr(cmd))
            except:
                self.logger.debug('unable to parse json data')
                break

            self.exec_cmd(cmd)

    def finish(self):
        self.logger.debug('finish')
        servo_manager = ServoManager()
        servo_manager.init_sequence()
