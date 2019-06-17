#!/usr/bin/env python
import subprocess
import threading


def VagrantUP():
    command = subprocess.Popen(["vagrant","up"],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        lines = command.stdout.readline()
        if not lines:
            break
        print(lines.rstrip())


th = threading.Thread(target=VagrantUP)
th.start()
th.join()
#https://living-sun.com/es/python/734175-python-subprocess-cannot-read-output-of-airodump-nd-mon0-python-subprocess-aircrack-ng.html