#!/usr/bin/python

import time
import signal
import subprocess
import sys
import ConfigParser
import random

if len(sys.argv) < 3:
    print "expect 1 argument: $target $interval"
    sys.exit(1)

config = ConfigParser.RawConfigParser()
config.read('config.ini')
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
    interval = float(para)
except ValueError:
    print "interval cannot be parsed!!Aborting.."
    sys.exit(1)

try:
    exclude_targets = config.get('injection', sys.argv[1] + '_target').strip('"')\
        .split(' ')
except:
    print "target not exists!"
    sys.exit(1)

#targets = []
#for target in all_targets:
#    if target not in exclude_targets:
#        targets.append(target)
targets = exclude_targets


def signal_handler(signal, frame):
    # os.system('sudo tc qdisc del dev eth0 root')
    subprocess.Popen(['sudo', 'tc', 'qdisc', 'del', 'dev', 'eth0', 'root'],
                     stdout=subprocess.PIPE).wait()
    sys.exit(0)
    #    os.system('sudo tc qdisc add dev eth0 root netem latency 30%')


signal.signal(signal.SIGTERM, signal_handler)
# subprocess.Popen(['sudo', 'tc', 'qdisc',
#                   'add', 'dev', 'eth0', 'root', 'netem', 'latency', '30%'],
#                  stdout=subprocess.PIPE)
#
# os.system('sudo tc qdisc del dev eth0 root')
rate = 0.0
command_set = []
# command_set.append("sudo tc qdisc add dev eth0 root handle 1: prio".split())
# command_set.append("sudo tc qdisc add dev eth0 parent 1:3 handle 30: tbf rate 20kbit \
#                    buffer 1600 limit 3000".split())
#
# latency_command = "sudo tc qdisc add dev eth0 parent 30:1 handle 31: netem latency " \
#    + str(rate) + "%"

#Started from 0.1 because no way to start from 0
latency_command = "sudo tc qdisc add dev eth0 root netem delay 0.1ms 0.1ms distribution normal"
command_set.append(latency_command.split())
# for target in targets:
#     s = "sudo tc filter add dev eth0 protocol ip parent 1:0 prio 3 \
#         u32 match ip dst " + target + "/32 flowid 1:3"
#     command_set.append(s.split())
#     s = "sudo tc filter add dev eth0 protocol ip parent 1:0 prio 3 \
#         u32 match ip src " + target + "/32 flowid 1:3"
#     command_set.append(s.split())

for command in command_set:
     subprocess.Popen(command, stdout=subprocess.PIPE).wait()

expo_scale = 1
while True:
    time.sleep(interval)
    if rate < 20000:
        scale = 2.0
        if _random:
            if random.random() > 0.5:
                scale = 0.0
        if exponecial:
            scale = expo_scale
            expo_scale += 1.0
        rate += scale
        # latency_command = "sudo tc qdisc change dev eth0 parent 30:1 handle 31: netem corrupt " \
        #     + str(rate) + "%"
        if rate > 0:
            latency_command = "sudo tc qdisc change dev eth0 root netem delay " + str(rate) + "ms 20ms distribution normal"
            subprocess.Popen(latency_command.split(), stdout=subprocess.PIPE).wait()
