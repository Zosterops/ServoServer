
import json
import logging
import SocketServer

class ServoServerHandler(SocketServer.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('ServoServerHandler')
        self.logger.debug('__init__')
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def get_cmd_json(self):
        data = ""
        char = self.request.recv(1)
        while char != ';':
            data += char
            char = self.request.recv(1)
        return data

    def setup(self):
        self.logger.debug('setup')

    def handle(self):
        self.logger.debug('handle')
        while True:
            data = self.get_cmd_json()
            self.logger.debug('json raw data : %s' % repr(data))

            try:
                cmd = json.loads(data)
                print cmd
            except:
                self.logger.debug('unable to parse json data')
                break


    def finish(self):
        self.logger.debug('finish')
