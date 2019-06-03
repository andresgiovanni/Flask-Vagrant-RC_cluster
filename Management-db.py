#!/usr/bin/env python
import json
import os
from pprint import pprint

JSONFILE="/home/cherno/Servidores/Flask-Vagrant-RC_cluster/DB.json"
VM = {'Web': 'Not create','DB': 'Not create'}

def readjson():
    if os.stat(JSONFILE).st_size == 0:
        print ("Vacio")
    else:
        with open(JSONFILE) as data_file:    
            data = json.load(data_file)
        pprint(data)

#def writejson(proyect, path, VM)
def writejson():
    data = {}
    if os.stat(JSONFILE).st_size == 0:
        data['Ubuntu'] = []
        data['Ubuntu'].append({'Proyecto': 'Ubuntu', 'Ruta': '/home/cherno/vagran/Ubuntu'})    
        with open(JSONFILE, 'w') as file_dest:
            json.dump(data, file_dest, sort_keys=True, indent=4)
    else:
        with open(JSONFILE, 'r') as file_orig:    
            data = json.load(file_orig)
        data['Centos'] = []
        data['Centos'].append({'Proyecto': 'Centos', 'Ruta': '/home/cherno/vagran/Centos', 'Status VM': [VM]})    
        with open(JSONFILE, 'w') as file_dest:
            json.dump(data, file_dest, sort_keys=True, indent=4)

#def deletejson(proyect)
def deletejson():
    data = {}    
    with open(JSONFILE, 'r') as file_orig:    
        data = json.load(file_orig)
        del data["a"]
    with open(JSONFILE, 'w') as file_dest:
        json.dump(data, file_dest, sort_keys=True, indent=4)

writejson()
#deletejson()
readjson()
#check()