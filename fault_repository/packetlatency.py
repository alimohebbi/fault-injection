#!/usr/bin/python
import inspect
import os
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

config = Config().config
all_targets = config.get('injection', 'all_targets').strip('"').split(' ')

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
    rate = int(para)
except ValueError:
    print "interval cannot be parsed!!Aborting.."
    sys.exit(1)

targets = []
for target in all_targets:
    targets.append(target)

def signal_handler(signal, frame):
    subprocess.Popen(['sudo', 'tc', 'qdisc', 'del', 'dev', 'eth0', 'root'],
                     stdout=subprocess.PIPE).wait()
    sys.exit(0)


signal.signal(signal.SIGTERM, signal_handler)
command_set = []

base = rate + 23.5
command_set.append("sudo tc qdisc add dev eth0 handle 1: root htb")
command_set.append("sudo tc class add dev eth0 parent 1: classid 1:1 htb rate 1000Mbps")
command_set.append("sudo tc class add dev eth0 parent 1:1 classid 1:11 htb rate 100Mbps")
command_set.append("sudo tc class add dev eth0 parent 1:1 classid 1:12 htb rate 100Mbps")
command_set.append(
    "sudo tc qdisc add dev eth0 parent 1:11 handle 10: netem delay " + str(base) + "ms " + str(rate) + "ms")
for ip in targets:
    command_set.append("sudo tc filter add dev eth0 protocol ip prio 1 u32 match ip dst " + ip + " flowid 1:11")
    command_set.append("sudo tc filter add dev eth0 protocol ip prio 1 u32 match ip src " + ip + " flowid 1:11")
command_set.append("sudo tc filter add dev eth0 protocol ip prio 2 u32 match ip src 0.0.0.0/0 flowid 1:12")
command_set.append("sudo tc filter add dev eth0 protocol ip prio 2 u32 match ip src 0.0.0.0/0 flowid 1:12")
command_set = [s.split() for s in command_set]

for command in command_set:
    subprocess.Popen(command, stdout=subprocess.PIPE).wait()

while True:
    time.sleep(300)
