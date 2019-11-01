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
all_targets = config.get('injection', 'all_targets').strip('"').split(' ')

try:
    exclude_targets = config.get('injection', sys.argv[1] + '_target').strip('"')\
        .split(' ')
except:
    print "target not exists!"
    sys.exit(1)

targets = []
for target in all_targets:
    if target not in exclude_targets:
        targets.append(target)


def signal_handler(signal, frame):
    # os.system('sudo tc qdisc del dev eth0 root')
    subprocess.Popen(['sudo', 'tc', 'qdisc', 'del', 'dev', 'eth0', 'root'],
                     stdout=subprocess.PIPE).wait()
    sys.exit(0)
    #    os.system('sudo tc qdisc add dev eth0 root netem corrupt 30%')


signal.signal(signal.SIGTERM, signal_handler)
# subprocess.Popen(['sudo', 'tc', 'qdisc',
#                   'add', 'dev', 'eth0', 'root', 'netem', 'corrupt', '30%'],
#                  stdout=subprocess.PIPE)
#
# os.system('sudo tc qdisc del dev eth0 root')
command_set = []
command_set.append("sudo tc qdisc add dev eth0 root handle 1: prio".split())
command_set.append("sudo tc qdisc add dev eth0 parent 1:3 handle 30: tbf rate 20kbit \
buffer 1600 limit 3000".split())

latency_command = "sudo tc qdisc add dev eth0 parent 30:1 handle 31: netem latency \
    delay 0ms 500ms"
command_set.append(latency_command.split())
for target in targets:
    s = "sudo tc filter add dev eth0 protocol ip parent 1:0 prio 3 \
              u32 match ip dst " + target + "/32 flowid 1:3"
    command_set.append(s.split())
    s = "sudo tc filter add dev eth0 protocol ip parent 1:0 prio 3 \
              u32 match ip src " + target + "/32 flowid 1:3"
    command_set.append(s.split())

for command in command_set:
    subprocess.Popen(command, stdout=subprocess.PIPE).wait()

while True:
    time.sleep(36)
