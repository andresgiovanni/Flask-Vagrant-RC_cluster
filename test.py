#!/usr/bin/env python
import subprocess
import time
import threading

stop_output = False

def f(p):
    global stop_output
    while True:
        l = p.stdout.readline()
        if not l or stop_output:
            break
        print(l.rstrip())   # or whatever you want to do with the line

airodump = subprocess.Popen(["vagrant","up"],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
#t = threading.Thread(target=f,args=(airodump,))
#t.start()
#time.sleep(145)
# kill the process and stop the display after 10 seconds whatever happens
#airodump.terminate()
#stop_output = True
#https://living-sun.com/es/python/734175-python-subprocess-cannot-read-output-of-airodump-nd-mon0-python-subprocess-aircrack-ng.html