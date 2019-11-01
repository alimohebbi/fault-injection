#!/usr/bin/python

import time
import signal
import subprocess
import sys
import ConfigParser

if len(sys.argv) < 2:
    print "expect 1 argument: $target"
    sys.exit(1)

config = ConfigParser.RawConfigParser()
config.read('config.ini')

try:
    targets = config.get('injection', sys.argv[1] + '_target').strip('"')\
        .split(' ')
except:
    print "target not exists!"
    sys.exit(1)


def signal_handler(signal, frame):
    inactive()
    sys.exit(0)
    #    os.system('sudo tc qdisc add dev eth0 root netem corrupt 30%')

signal.signal(signal.SIGTERM, signal_handler)


def active():
    active_com = []
    for target in targets:
        s = "sudo ip route add blackhole " + target + "/32"
        active.append(s.split())
    for command in active_com:
        subprocess.Popen(command, stdout=subprocess.PIPE).wait()


def inactive():
    inactive_com = []
    for target in targets:
        s = "sudo ip route delete " + target + "/32"
        inactive.append(s.split())
    for command in inactive_com:
        subprocess.Popen(command, stdout=subprocess.PIPE).wait()

while True:
    active()
    time.sleep(10)
    inactive()
    time.sleep(10)
