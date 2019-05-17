#!/usr/local/bin/python
from flask import Flask, request
import os

app = Flask(__name__)   

@app.route("/vagrant_init")
def crearInit():
  Path = '$HOME'
#  os.mkdir("vagrant")
#  os.chdir("vagrant")
# Path = '/home/vagrant'
#  vagrantInit= 'vagrant init '
#  PathVagrant= path + 'Vagrantfile'
#  if os.path.exists(Path):
#    if os.path.exists(PathVagrant):
#      myCmd = os.popen(vagrantInit).read()
#  else:
#    print("Creando ruta...")
#    os.mkdir(Path)
#    os.chdir(Path)
#    myCmd = os.popen(vagrantInit).read()
#    return 'Ready Vagrantfile \n\n{}\n'.format(myCmd)
  myCmd = os.popen("vagrant init").read()
  return 'Ready Vagrantfile \n\n{}\n'.format(myCmd)

@app.route("/vagrant_up")
@app.route("/vagrant_up/<name>")
def Vagrant_up(name = ''):
  Cmd = 'vagrant up ' +  name
  myCmd = os.popen(Cmd).read()

@app.route("/vagrant_halt")
@app.route("/vagrant_halt/<name>")
def Vagrant_halt(name = ''):
  Cmd = 'vagrant halt ' +  name
  myCmd = os.popen(Cmd).read()
  return '\n{}\n'.format(myCmd)

@app.route("/vagrant_destroy")
@app.route("/vagrant_destroy/<name>")
def Vagrant_destroy(name = ''):
  Cmd = 'vagrant destroy -f ' +  name 
  myCmd = os.popen(Cmd).read()
  return '\n{}\n'.format(myCmd)

@app.route("/box_list")
def listBox():
  Cmd = 'vagrant box list'
  myCmd = os.popen(Cmd).read()
  return 'Box list: \n\n{}\n'.format(myCmd)

# mejorar peticion
@app.route("/box_add")
@app.route("/box_add/<name>")
def addBox(name = 'bento/ubuntu-18.04'):
  Cmd = 'vagrant box add ' +  name
#  myCmd = os.popen(Cmd).read()
  return 'Box add: {}\n'.format(Cmd)

if __name__ == "__main__":
  app.run(debug=True,  port=8000)
