
import json
import logging
import SocketServer

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
        Takes char by char data into the buffer
        Stop when ';' it's seen or when recv() returns 0
        """
        data = ""
        char = self.request.recv(1)
        while char != ';' and len(char) != 0:
            data += char
            char = self.request.recv(1)
        return data

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

    def finish(self):
        self.logger.debug('finish')
