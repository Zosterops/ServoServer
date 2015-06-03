
import logging
import subprocess
import threading

class CameraThread(threading.Thread):
    """
    Thread who is launching a subprocess
    """

    def __init__(self, ip):
        """
        init thread with command
        """
        self.logger = logging.getLogger('CameraThread')
        self.logger.debug('__init__')
        self.logger.debug('client = %s' % ip)
        self.ip = ip
        threading.Thread.__init__(self)

    def run(self):
        """
        run the subprocess
        """
        self.logger.debug('run')
        self.raspi_p = subprocess.Popen("raspivid -t 0 -h 720 -w 1080 -fps 30 -b 2000000 -o -".split(), stdout=subprocess.PIPE)
        # MyComputerIsAwesome
        cmd = "gst-launch-1.0 -v fdsrc fd=0 ! h264parse ! rtph264pay ! udpsink host=%s port=5004" % self.ip
        self.gst_p = subprocess.Popen(cmd.split(),
                    stdin=self.raspi_p.stdout)
        # self.raspi_p = subprocess.Popen("cat /dev/urandom".split(), stdout=subprocess.PIPE, shell=True)
        # self.gst_p = subprocess.Popen("grep youpiyayaya".split(), stdin=self.raspi_p.stdout)
        self.logger.debug('process launched, wait for end....')
        ret = self.raspi_p.wait()
        self.logger.debug('return value raspi_p : %d' % ret)
        ret = self.gst_p.wait()
        self.logger.debug('return value gst_p : %d' % ret)

    def arret(self):
        """
        stop the subprocess
        """
        self.logger.debug('arret')
        self.raspi_p.kill()
        self.gst_p.kill()


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

    def start(self, ip):
        """
        Start the camera
        """
        self.logger.debug('start')
        self.logger.debug(ip)
        if self.running is False:
            self.thread = CameraThread(ip)
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
            self.thread.arret()
            self.running = False
        else:
            self.logger.debug('Camera is not running')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')
    manager = CameraManager()
    manager.start("youp")
    import time
    time.sleep(4)
    manager.stop()
    while True:
        pass
