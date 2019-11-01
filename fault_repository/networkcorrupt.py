#!/usr/bin/python

import ConfigParser
import random
import signal
import subprocess
import sys
import time

if len(sys.argv) < 3:
    print "expect 1 argument: $target $interval"
    sys.exit(1)

config = ConfigParser.RawConfigParser()
config.read('config.ini')

_random = False
exponential = False
para = sys.argv[2]

print para
if 'random' in para:
    _random = True
    para = para.replace('random', '')

if 'expo' in para:
    exponential = True
    para = para.replace('expo', '')

print para
try:
    interval = float(para)
except ValueError:
    print "interval cannot be parsed!!Aborting.."
    sys.exit(1)

try:
    exclude_targets = config.get('injection', sys.argv[1] + '_target').strip('"') \
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
rate = 0.0
command_set = []

corrupt_command = "sudo tc qdisc add dev eth0 root netem corrupt " + str(rate) + "%"
command_set.append(corrupt_command.split())

for command in command_set:
    subprocess.Popen(command, stdout=subprocess.PIPE).wait()

expo_scale = 0.1
while True:
    time.sleep(interval)
    if rate < 40:
        scale = 0.1
        if _random:
            if random.random() > 0.5:
                scale = 0.0
        if exponential:
            scale = expo_scale
            expo_scale += 0.1
        rate += scale
        corrupt_command = "sudo tc qdisc change dev eth0 root netem corrupt " + str(rate) + "%"
        subprocess.Popen(corrupt_command.split(), stdout=subprocess.PIPE).wait()
