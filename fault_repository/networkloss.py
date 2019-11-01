#!/usr/bin/python

import ConfigParser
import inspect
import os
import random
import signal
import subprocess
import sys
import time

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from config import Config

if len(sys.argv) < 3:
    print "expect 1 argument: $target $interval"
    sys.exit(1)

config = Config()
all_targets = config.get('injection', 'all_targets').strip('"').split(' ')

_random = False
exponecial = False
para = sys.argv[2]

print para
if 'random' in para:
    _random = True
    para = para.replace('random', '')

if 'expo' in para:
    exponecial = True
    para = para.replace('expo', '')

print para
try:
    interval = int(para)
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


signal.signal(signal.SIGTERM, signal_handler)

rate = 0.1
command_set = []

loss_command = "sudo tc qdisc add dev eth0 root netem loss " + str(rate) + "%"
command_set.append(loss_command.split())

for command in command_set:
    subprocess.Popen(command, stdout=subprocess.PIPE).wait()

expo_scale = 1
while True:
    time.sleep(interval)
    if rate < 40:
        scale = 1
        if _random:
            if random.random() > 0.5:
                scale = 0
        if exponecial:
            scale = expo_scale
            expo_scale += 1
        rate += scale
        loss_command = "sudo tc qdisc change dev eth0 root netem loss " + str(rate) + "%"
        subprocess.Popen(loss_command.split(), stdout=subprocess.PIPE).wait()
