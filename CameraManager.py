
import logging
import socket
import picamera
import time
import threading
import io
import struct

class ImageSender(threading.Thread):

    def __init__(self, conn, manager):
        super(ImageSender, self).__init__()
        self.logger = logging.getLogger('ImageSender')
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.conn = conn
        self.manager = manager
        self.start()

    def run(self):
        while not self.terminated:
            if self.event.wait(1):
                try:
                    size = self.stream.tell()
                    self.stream.seek(0)
                    with self.manager.lock_conn:
                        self.conn.send(struct.pack('<I', size))
                        self.conn.send(self.stream.read())
                except:
                    self.manager.done = True
                finally:
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    with self.manager.lock_pool:
                        self.manager.pool.append(self)


class CameraManager:
    """
    Used to manage image stream
    """

    def __init__(self, host='0.0.0.0', port=1993, n_sender=4):
        self.logger = logging.getLogger('CameraManager')
        self.logger.debug('__init___')
        self.port = port
        self.host = host
        self.n_sender = n_sender
        self.done = False

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
            self.serv_flux(conn, addr)
            conn.close()
        except:
            pass
        finally:
            self.close()

    def create_senders(self, conn):
        self.logger.debug('create_senders')
        self.lock_pool = threading.Lock()
        self.lock_conn = threading.Lock()
        self.pool = []
        for i in range(self.n_sender):
            t = ImageSender(conn, self)
            self.logger.debug('create thread : %s' % repr(t))
            self.pool.append(t)

    def stop_senders(self):
        self.logger.debug('stop_senders')
        while self.pool:
            with self.lock_pool:
                processor = self.pool.pop()
            self.logger.debug('stop thread : %s' % repr(processor))
            processor.terminated = True
            processor.join()

    def streams(self):
        while not self.done:
            with self.lock_pool:
                if self.pool:
                    processor = self.pool.pop()
                else:
                    processor = None
            if processor:
                yield processor.stream
                processor.event.set()
            else:
                # when the pool is starved, wait a while for it to refill
                time.sleep(0.1)

    def serv_flux(self, conn, addr):
        self.logger.debug('serv_flux')
        self.create_senders(conn)
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.framerate = 30
            camera.start_preview()
            camera.capture_sequence(self.streams(), use_video_port=True)
        self.stop_senders()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="CameraManager test")
    parser.add_argument('port', type=int, default=3991, help="port in which launch the server")
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')
    manager = CameraManager(port=args.port, n_sender=4)
    manager.start()

