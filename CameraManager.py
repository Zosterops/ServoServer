
import logging
import socket

class CameraManager:
    """
    Used to manage image stream
    """

    def __init__(self, host='0.0.0.0', port=1993):
        self.logger = logging.getLogger('CameraManager')
        self.logger.debug('__init___')
        self.port = port
        self.host = host

    def create_socket(self):
        self.logger.debug('create_socket')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def bind(self):
        self.logger.debug('bind')
        self.socket.bind((self.host, self.port))

    def listen(self, n=1):
        self.logger.debug('listen')
        self.socket.listen(n)

    def accept(self):
        self.logger.debug('accept')
        return self.socket.accept()

    def close(self):
        self.logger.debug('close')
        self.socket.close()

    def start(self):
        self.logger.debug('start')
        self.create_socket()
        self.bind()
        self.listen()
        try:
            conn, addr = self.accept()
            conn.send("salut !")
            conn.close()
        except:
            pass
        finally:
            self.close()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="CameraManager test")
    parser.add_argument('port', type=int, default=3991, help="port in which launch the server")
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')
    manager = CameraManager(port=args.port)
    manager.start()

