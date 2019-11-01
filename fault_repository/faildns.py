#!/usr/bin/python

import time
import signal
import subprocess
import sys
import ConfigParser

if len(sys.argv) < 2:
    print "expect 1 argument: $target"
    sys.exit(1)

ports = {'ellis': 80,
         'bono': 5060,
         'sprout': 5054,
         'homestead': 8888,
         'homer': 8888,
         'ralf': 10888,
         'huawei1': 5672,
         'huawei2': 67,
         'huawei3': 67,
         'huawei4': 67,
         'huawei5': 67,
         'huawei6': 67,
         'huawei7': 67,
         'huawei8': 67,
         }

config = ConfigParser.RawConfigParser()
config.read('config.ini')

try:
    port = ports[sys.argv[1]]
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
    s = "sudo iptables -A INPUT -p tcp -m tcp --dport " + port + " -j DROP"
    active.append(s.split())
    s = "sudo iptables -A INPUT -p udp -m tcp --dport " + port + " -j DROP"
    active.append(s.split())
    for command in active_com:
        subprocess.Popen(command, stdout=subprocess.PIPE).wait()

def inactive():
    inactive_com = []
    s = "sudo iptables -D INPUT -p tcp -m tcp --dport " + port + " -j DROP"
    inactive.append(s.split())
    s = "sudo iptables -D INPUT -p udp -m tcp --dport " + port + " -j DROP"
    inactive.append(s.split())
    for command in inactive_com:
        subprocess.Popen(command, stdout=subprocess.PIPE).wait()

while True:
    active()
    time.sleep(10)
    inactive()
    time.sleep(10)
