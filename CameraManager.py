
import logging
import SocketServer
import picamera
import io

class CameraHandler(SocketServer.BaseRequestHandler):
    """
    CameraHandler handle every requests made by the user
    concerning the camera pictures
    """

    def __init__(self, request, client_address, server):
        """
        Construct a new 'CameraHandler' object
        """
        self.logger = logging.getLogger('CameraHandler')
        self.logger.debug('__init__')
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def setup(self):
        self.logger.debug('setup')

    def handle(self):
        """
        Handle every request made by the user
        """
        self.logger.debug('handle')
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            import time
            time.sleep(2)
            stream = io.RawIOBase()
            for _ in camera.capture_continuous(stream, 'jpeg'):
                size = stream.tell()
                stream.seek(0)
                stream.read()
                stream.seek(0)
                stream.truncate()
                self.logger.debug('size = %d' % size)



    def finish(self):
        self.logger.debug('finish')


class CameraManager:
    """
    Used to manage image stream
    """

    def __init__(self):
        self.logger = logging.getLogger('CameraManager')
        self.server = SocketServer.TCPServer(("0.0.0.0", 1993), CameraHandler)
        self.logger.debug('__init___')

    def start(self):
        self.logger.debug('start serving')
        try:
            self.server.serve_forever()
        except:
            pass
        self.stop()

    def stop(self):
        self.logger.debug('stop serving')
        self.server.shutdown()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')
    manager = CameraManager()
    manager.start()

