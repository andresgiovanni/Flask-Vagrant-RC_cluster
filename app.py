#!/usr/bin/env python
import os
import threading
import envConfig
import ManagementDB
import VagrantGest
from flask import Flask, render_template, request, jsonify
from werkzeug import secure_filename
from shutil import rmtree

# instancia del objeto Flask
app = Flask(__name__)

#curl -F 'file=@/home/cherno/Vagrantfile' http://localhost:8000/CrearProyecto
@app.route('/CrearProyecto', methods=['POST'])
@app.route('/CrearProyecto/<NameProyect>', methods=['POST'])
def upProyect(NameProyect='default'):
    path = envConfig.VAGRANTPROJECT + NameProyect
    if request.method == 'POST':
        if ManagementDB.ReadElemt(NameProyect) == True:
            #susceptible a mejoras
            return jsonify('Existe el proyeto: ' + NameProyect + '\n')
        else:
            #1) Creacion de folder
            os.mkdir(path)
            #2) Almacenaciento de Vagrantfile
            f = request.files['file']
            filename = secure_filename(f.filename)
            f.save(os.path.join(path, filename))
            #3) Registro en DB json
            # - VagrantGest.VagrantStatus(NameProyect) => devuelve el estado de VM en forma de Dicc.
            ManagementDB.WriteElemt(NameProyect, VagrantGest.VagrantStatus(NameProyect))
            return jsonify('Se creo proyecto: ' + NameProyect + '\n')

#curl http://localhost:8000/BorrarProyecto
@app.route('/BorrarProyecto')
@app.route('/BorrarProyecto/<NameProyect>')
def deleteProyect(NameProyect='default'):
    path = envConfig.VAGRANTPROJECT + NameProyect
    if ManagementDB.ReadElemt(NameProyect) == True:
        if VagrantGest.CheckVagrant(NameProyect):
            if VagrantGest.VmCreated(NameProyect)!='0':
            #1) Se destruyen maquinas
                VagrantGest.VagrantDestroy(NameProyect, '')
            #2) Se elimina folder
                rmtree(path)
            #3) Se actualiza la DB
                ManagementDB.DeleteElemt(NameProyect)
            else:
            #1) Se elimina folder
                rmtree(path)
            #2) Se actualiza la DB
                ManagementDB.DeleteElemt(NameProyect)
            return jsonify('El proyecto: ' + NameProyect + ' se elimino de DB\n')
        else:
            return jsonify('Existe en DB y pero no hay Vagrantfile\n')
    else:
        return jsonify('No existe en DB\n')

#curl http://localhost:8000/StatusProyecto
@app.route('/StatusProyecto')
@app.route('/StatusProyecto/<NameProyect>')
def statusProyect(NameProyect='default'):
    return  jsonify(ManagementDB.StatusElemt(NameProyect))

#curl http://localhost:8000/LevantarVM
@app.route('/LevantarVM')
@app.route('/LevantarVM/<NameProyect>')
@app.route('/LevantarVM/<NameProyect>/<VMs>')
def levantarVM(NameProyect='default', VMs='node-1'):
    if ManagementDB.ReadElemt(NameProyect) == True:
        if VagrantGest.CheckVagrant(NameProyect):
            threadUP = threading.Thread(target=VagrantGest.VagrantUP, args=(NameProyect, VMs))
            threadUP.start()
            threadUP.join()
            ManagementDB.WriteElemt(NameProyect, VagrantGest.VagrantStatus(NameProyect))
            return jsonify('Se esta creando la maquina\n')
        else:
            return jsonify('Existe en DB y pero no hay Vagrantfile\n')
    else:
        return jsonify('No existe en DB\n')

#curl http://localhost:8000/ApagarVM
@app.route('/ApagarVM')
@app.route('/ApagarVM/<NameProyect>')
@app.route('/ApagarVM/<NameProyect>/<VMs>')
def ApagarVM(NameProyect='default', VMs=''):
    if ManagementDB.ReadElemt(NameProyect) == True:
        if VagrantGest.CheckVagrant(NameProyect):
            return jsonify(VagrantGest.VagrantHalt(NameProyect, VMs))
            return jsonify(ManagementDB.WriteElemt(NameProyect, VagrantGest.VagrantStatus(NameProyect)))
        else:
            return jsonify('Existe en DB y pero no hay Vagrantfile\n')
    else:
        return jsonify('No existe en DB\n')

#curl http://localhost:8000/BorrarVM
@app.route('/BorrarVM')
@app.route('/BorrarVM/<NameProyect>')
@app.route('/BorrarVM/<NameProyect>/<VMs>')
def deleteVM(NameProyect='default', VMs=''):
    if ManagementDB.ReadElemt(NameProyect) == True:
        if VagrantGest.CheckVagrant(NameProyect):
            if VagrantGest.VmCreated(NameProyect)!='0':
            #1) Se destruyen maquinas
                VagrantGest.VagrantDestroy(NameProyect, VMs)
            #2) Actualizar DB
                ManagementDB.ModifyElemt(NameProyect, NameProyect, VagrantGest.VagrantStatus(NameProyect))
            #3) Respuesta
                return jsonify('Del proyecto: ' + NameProyect + ' se elimino ' + VMs + '\n')
            else:
            #3) Respuesta
                return jsonify('El proyecto: ' + NameProyect + ' no tiene VM creadas\n')
        else:
            return jsonify('Existe en DB y pero no hay Vagrantfile\n')
    else:
        return jsonify('No existe en DB\n')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0",  port=8000)
