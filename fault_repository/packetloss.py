#!/usr/bin/python

import time
import signal
import subprocess
import sys
import ConfigParser

from config import Config

if len(sys.argv) < 3:
    print "expect 1 argument: $target $interval"
    sys.exit(1)

config = Config().config

_random = False
exponential = False
para = sys.argv[2]

if 'random' in para:
    _random = True
    para = para.replace('random', '')

if 'expo' in para:
    exponential = True
    para = para.replace('expo', '')

try:
    rate = float(para)
except ValueError:
    print "interval cannot be parsed!!Aborting.."
    sys.exit(1)

try:
    exclude_targets = config.get('injection', sys.argv[1] + '_target').strip('"')\
        .split(' ')
except:
    print "target not exists!"
    sys.exit(1)

targets = exclude_targets


def signal_handler(signal, frame):
    # os.system('sudo tc qdisc del dev eth0 root')
    subprocess.Popen(['sudo', 'tc', 'qdisc', 'del', 'dev', 'eth0', 'root'],
                     stdout=subprocess.PIPE).wait()
    sys.exit(0)
    #    os.system('sudo tc qdisc add dev eth0 root netem corrupt 30%')


signal.signal(signal.SIGTERM, signal_handler)
command_set = []

loss_command = "sudo tc qdisc add dev eth0 root netem loss " + str(rate) + "%"
command_set.append(loss_command.split())

for command in command_set:
    subprocess.Popen(command, stdout=subprocess.PIPE).wait()

while True:
    time.sleep(300)
