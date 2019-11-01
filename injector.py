import ConfigParser
import os
import socket
import subprocess
import sys

from config import Config

config = Config().config
port = int(config.get('injection', 'port'))
BUFFER_SIZE = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', port))
# s.listen(1)

# conn = s.accept()
plst = []
while 1:
    data = s.recvfrom(BUFFER_SIZE)
    if not data or type(data) != tuple:
        for p in plst:
            p.terminate()
        break
    if data[0] == "stop":
        for p in plst:
            p.terminate()
        break
    if data != "stop":
        print "recv: " + str(data)
        faults = eval(data[0])
       # time.sleep(5400)
        for fault in faults:
            full_command = fault.split('_')
            candidates = os.listdir('fault_repository')
            targets = filter(lambda x: full_command[0] in x, candidates)
            if len(targets) != 1:
                print "Fault not found or more than 1 !! Aborting..."
                sys.exit(1)
            full_command[0] = 'fault_repository/' + targets[0]
            p = subprocess.Popen(full_command, stdout=subprocess.PIPE)
            plst.append(p)
