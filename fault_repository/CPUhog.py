#!/usr/bin/python

import random
import signal
import sys
import time
from multiprocessing import Process, Value

if len(sys.argv) < 3:
    print "expect 1 argument: $target $interval"
    sys.exit(1)


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
    interval = int(para)
except ValueError:
    print "interval cannot be parsed!!Aborting.."
    sys.exit(1)

flag = Value('b', True)


def signal_handler(signal_, frame):
    global flag
    flag.value = False
    sys.exit(0)


signal.signal(signal.SIGTERM, signal_handler)

cpuinfo_raw = open('/proc/cpuinfo').readlines()
cpuinfo = filter(lambda x: x is not None,
                 [float(line.split(':')[1].strip(' ')) * 3000 if 'MHz' in line else None for line in cpuinfo_raw])

print cpuinfo

cpunum = len(cpuinfo)

percent_init = 0
thread_pool = []
sleeptime_lst = []
loop_lst = []


def cpuhog(loop, sleep):
    while flag.value:
        looptimes = loop.value
        for i in range(looptimes):
            pass

        time.sleep(sleep.value)
    sys.exit(0)


for i in range(cpunum):
    cpu_clock = float(cpuinfo[i])
    loop_init = int(cpu_clock * percent_init / 100.0)
    sleep_init = cpu_clock - loop_init

    looptime = Value('i', loop_init)
    sleeptime = Value('d', sleep_init * 1.0 / cpu_clock)

    p = Process(target=cpuhog, args=(looptime, sleeptime,))
    thread_pool.append(p)
    sleeptime_lst.append(sleeptime)
    loop_lst.append(looptime)

for i in range(cpunum):
    thread_pool[i].start()

percent = percent_init
expo_scale = 1

while flag.value:
    time.sleep(interval)
    if percent < 90:
        scale = 1
        if _random:
            if random.random() > 0.5:
                scale = 0
        if exponential:
            scale = expo_scale
            expo_scale += 1
        percent += scale

    for i in range(cpunum):
        cpu_clock = float(cpuinfo[i])
        loop_new = int(cpu_clock * percent / 100.0)
        sleep_new = cpu_clock - loop_new

        loop_lst[i].value = loop_new
        sleeptime_lst[i].value = sleep_new * 1.0 / cpu_clock

#    print percent, [v.value for v in loop_lst],
# [v.value for v in sleeptime_lst]

for p in thread_pool:
    p.terminate()
