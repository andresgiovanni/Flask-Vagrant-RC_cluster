#!/usr/bin/env python
import json
import os
import envConfig
import ManagementDB

# Los posibles estados de una maquina son
# not created, running, saved, poweroff
def VagrantStatus():
    VMs = {}
    myCmd = os.popen("vagrant status | grep \) | tr -s ' '").read()
    lineas = myCmd.split("\n")
    lineas.pop(len(lineas)-1)
    print lineas
    for linea in lineas:
        data = linea.split()
        if 'not created' in linea:
            VM = {data[0]:{"Status" : "not created", "Hipervisor" : data[3]}}
            VMs.update(VM) 
        else:
            VM = {data[0]:{"Status" : data[1], "Hipervisor" : data[2]}}
            VMs.update(VM)
    return VMs
#VagrantStatus()
ManagementDB.WriteElemt("kubernetes", VagrantStatus())