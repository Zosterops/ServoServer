#!/usr/bin/env python2

import argparse
import logging
import SocketServer
from ServoServerHandler import ServoServerHandler
from ServoManager import ServoManager

parser = argparse.ArgumentParser(description="Server to comunicate with the servo motors")
parser.add_argument('port', type=int, default=1993, help="port in which launch the server")
args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')

servo_manager = ServoManager(gpio_up_down=3, gpio_right_left=2) # singleton
server = SocketServer.TCPServer(("0.0.0.0", args.port), ServoServerHandler)
server.serve_forever()