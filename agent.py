import socket
import ConfigParser
import sys

config = ConfigParser.RawConfigParser()
config.read('config.ini')
f_list = config.get('injection', 'f_list').strip('"').split(' ')
port = int(config.get('injection', 'port'))
ips = config.get('injection', 'ips_injection').strip('"').split(' ')

if len(sys.argv) < 2 or (sys.argv[1] != 'start' and sys.argv[1] != 'stop'):
    print "expect 1 argument: start/stop"
    sys.exit(1)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if sys.argv[1] == 'stop':
    for ip in ips:
        print "sending stop to:" + str(ip)
        for i in range(20):
            s.sendto('stop', (ip, port))
    sys.exit(0)

faults = {}
for term in f_list:
    term_lst = term.split('=')
    faults[term_lst[0]] = term_lst[1].split(',')
print faults
for ip in faults:
    print "sending fault requset \"" + str(faults[ip]) + "\" to " + str(ip)
    s.sendto(str(faults[ip]), (ip, port))
