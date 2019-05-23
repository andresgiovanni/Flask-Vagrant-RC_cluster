import os, sys

path=sys.argv[1]
name=sys.argv[2]
init="vagrant init " + name
vagrantservices="/home/cherno/vagrantservices"
pathDB="/home/cherno/vagrantservices/VagrantList.cfg"
# Este scrip simula como crea un nuevo proyecto (Vagranfile)

def CreateFolder(path, name):
  os.mkdir(path)
  os.chdir(path)
  cli = os.popen(init).read()

def DeleteFolder(path):
  os.popen("rm -R " + path)

def DeleteItenDB(path):
  VagrantList = open(pathDB,"r") 
  lineas = VagrantList.readlines()
  VagrantList.close()
  VagrantList = open(pathDB,"w")
  for linea in lineas:
    if linea!=path+"\n":
      VagrantList.write(linea)
  VagrantList.close()

def UpdataItenDB(path):
  os.chdir(vagrantservices)
  VagrantList = open(pathDB, "a")
  VagrantList.writelines(path+"\n")
  VagrantList.close()

def CheckDB(path):
  VagrantList=open(pathDB, "r")
  for i,linea in enumerate(VagrantList):
    if (linea.strip("\n")==path):
      print linea.strip("\n")
      print i 
      break 
  VagrantList.close()

#CreateFolder(path, name)
#UpdataItenDB(path)
DeleteItenDB(path)
#CheckDB(path)