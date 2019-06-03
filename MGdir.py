#!/usr/bin/env python
import os, sys

vagrantservices="/home/cherno/vagrantservices"
pathDB="/home/cherno/vagrantservices/VagrantList.cfg"
# Este scrip simula como crea un nuevo proyecto (Vagranfile)

def CreateProyect(path):
  if CheckDB(path):
    return True
  else:
    CreateFolder(path)
    UpdataItenDB(path) 
    return False
    

def CreateFolder(path):
  os.mkdir(path)
  return "Se creo el proyecto de manera correcta"

def InitVagrantfile(name):
  init="vagrant init " + name
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
#      print linea.strip("\n")
#      print i
      return True 
      break   
  return False
  VagrantList.close()

#CreateProyect(path, name)
#UpdataItenDB(path)
#DeleteItenDB(path)
#CheckDB(path)