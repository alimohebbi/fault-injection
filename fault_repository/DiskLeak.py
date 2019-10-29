#!/usr/bin/python

import time
import signal
import subprocess
import os
import sys

diskcnt = 1
p_pool = []


def signal_handler(signal_, frame):
    global p_pool
    for p in p_pool:
        os.killpg(p.pid, signal.SIGTERM)
        p = subprocess.Popen(['sudo', 'rm', '/burn'], stdout=subprocess.PIPE)
        p.wait()
    sys.exit(0)
#    os.system('sudo tc qdisc add dev eth0 root netem corrupt 30%')


signal.signal(signal.SIGTERM, signal_handler)

for i in range(diskcnt):
    p = subprocess.Popen(['sudo', 'sh', 'fault_injection/ \
                          fault_repository/sub_scripts/DiskLeak.sh'],
                         stdout=subprocess.PIPE, preexec_fn=os.setsid)
    p_pool.append(p)

print p_pool
# os.system('sudo tc qdisc del dev eth0 root')

while True:
    time.sleep(60)
