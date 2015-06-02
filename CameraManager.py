
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
        self.raspi_p = subprocess.Popen("raspivid -t 0 -h 720 -w 1080 -fps 30 -b 2000000 -o -".split(" "), stdout=subprocess.PIPE)
        self.gst_p = subprocess.Popen("gst-launch-1.0 -v fdsrc fd=0 ! h264parse ! rtph264pay ! udpsink host=MyComputerIsAwesome port=5004".split(" "), )
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

    def __init__(self):
        self.logger = logging.getLogger('CameraManager')
        self.logger.debug('__init__')
        self.running = False

    def start(self, cmd):
        """
        Start the camera
        """
        self.logger.debug('start')
        if self.running is False:
            self.thread = CameraThread(cmd)
            self.thread.start()
            self.running = True
        else:
            self.logger.debug('camera is already running')

    def stop(self):
        """
        Stop the camera
        """
        self.logger.debug('stop')
        if self.running is True:
            self.thread.stop()
            self.running = False
        else:
            self.logger.debug('Camera is not running')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')
    manager = CameraManager(cmd="yes oui")
    manager.start()
    manager.start()

    import time
    time.sleep(3)
    manager.stop()
    manager.stop()
    manager.start()
