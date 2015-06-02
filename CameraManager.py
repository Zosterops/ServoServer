
import logging
import subprocess
import threading

class CameraThread(threading.Thread):
    """
    Thread who is launching a subprocess
    """

    def __init__(self, cmd):
        """
        init thread with command
        """
        self.logger = logging.getLogger('CameraThread')
        self.logger.debug('__init__')
        self.cmd = cmd
        threading.Thread.__init__(self)

    def run(self):
        """
        run the subprocess
        """
        self.logger.debug('run')
        self.process = subprocess.Popen(self.cmd.split(" "), stdout=subprocess.PIPE, shell=True)
        self.logger.debug('process launched, wait for end....')
        ret = self.process.wait()
        self.logger.debug('return value : %d' % ret)

    def stop(self):
        """
        stop the subprocess
        """
        self.logger.debug('stop')
        self.process.terminate()


class CameraManager:
    """
    Used to manage the Camera
    Singleton
    """

    __shared_state = {}

    def __init__(self, cmd=None):
        self.__dict__ = self.__shared_state
        if cmd is not None:
            self.logger = logging.getLogger('CameraManager')
            self.logger.debug('__init__')
            self.cmd = cmd

    def start(self):
        """
        Start the camera
        """
        self.logger.debug('start')
        self.thread = CameraThread(self.cmd)
        self.thread.start()

    def stop(self):
        """
        Stop the camera
        """
        self.logger.debug('stop')
        self.thread.stop()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')
    manager = CameraManager(cmd="yes oui")
    manager.start()

    import time
    time.sleep(3)
    manager.stop()
