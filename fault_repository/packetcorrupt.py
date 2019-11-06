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

# Get interface: for host sw, otherwise eth0
interfaces = os.listdir('/sys/class/net/')
sw = filter(lambda s: s.startswith('sw'), interfaces)
if len(sw) > 0:
    dev = sw[0]
    # host = True
    host = False
else:
    dev = 'eth0'
    host = False


def signal_handler(signal, frame):
    # os.system('sudo tc qdisc del dev eth0 root')
    subprocess.Popen(['sudo', 'tc', 'qdisc', 'del', 'dev', dev, 'root'],
                     stdout=subprocess.PIPE).wait()
    sys.exit(0)
    #    os.system('sudo tc qdisc add dev eth0 root netem corrupt 30%')


signal.signal(signal.SIGTERM, signal_handler)
command_set = []

command_set.append("sudo tc qdisc add dev " + dev + " handle 1: root htb")
command_set.append("sudo tc class add dev " + dev + " parent 1: classid 1:1 htb rate 1000Mbps")
command_set.append("sudo tc class add dev " + dev + " parent 1:1 classid 1:11 htb rate 100Mbps")
command_set.append("sudo tc class add dev " + dev + " parent 1:1 classid 1:12 htb rate 100Mbps")
command_set.append("sudo tc qdisc add dev " + dev + " parent 1:11 handle 10: netem corrupt " + str(rate) + "%")
# for ip in exclude_targets:
#     command_set.append("sudo tc filter add dev eth0 protocol ip prio 1 u32 match ip dst " + ip + " flowid 1:11")
for ip in targets:
    command_set.append("sudo tc filter add dev " + dev + " protocol ip prio 1 u32 match ip dst " + ip + " flowid 1:11")
    command_set.append("sudo tc filter add dev " + dev + " protocol ip prio 1 u32 match ip src " + ip + " flowid 1:11")
command_set.append("sudo tc filter add dev " + dev + " protocol ip prio 2 u32 match ip src 0.0.0.0/0 flowid 1:12")
command_set.append("sudo tc filter add dev " + dev + " protocol ip prio 2 u32 match ip src 0.0.0.0/0 flowid 1:12")
command_set = [s.split() for s in command_set]

for command in command_set:
    subprocess.Popen(command, stdout=subprocess.PIPE).wait()

while True:
    if host:
        time.sleep(60)
        command = "sudo tc qdisc change dev " + dev + " parent 1:11 handle 10: netem corrupt " + str(rate) + "%"
        subprocess.Popen(command.split(), stdout=subprocess.PIPE).wait()
        time.sleep(60)
        command = "sudo tc qdisc change dev " + dev + " parent 1:11 handle 10: netem corrupt 0%"
        subprocess.Popen(command.split(), stdout=subprocess.PIPE).wait()
    else:
        time.sleep(300)
