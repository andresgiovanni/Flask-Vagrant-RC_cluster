#!/usr/bin/env python
import subprocess
import threading

def VagrantUP(VM):
    command = subprocess.Popen(["vagrant","up",VM],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        lines = command.stdout.readline()
        if not lines:
            break
        return(lines.rstrip())


th = threading.Thread(target=VagrantUP, args=('node-1',))
th.start()
th.join()
#https://living-sun.com/es/python/734175-python-subprocess-cannot-read-output-of-airodump-nd-mon0-python-subprocess-aircrack-ng.html