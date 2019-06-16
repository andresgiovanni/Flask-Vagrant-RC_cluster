#!/usr/bin/env python
import os
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
            return 'Existe el proyeto: ' + NameProyect + '\n'
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
            return 'Se creo proyecto: ' + NameProyect + '\n'

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
            return 'El proyecto: ' + NameProyect + ' se elimino de DB\n'
        else:
            return 'Existe en DB y pero no hay Vagrantfile\n'
    else:
        return 'No existe en DB\n'

#curl http://localhost:8000/StatusProyecto
@app.route('/StatusProyecto')
@app.route('/StatusProyecto/<NameProyect>')
def statusProyect(NameProyect='default'):
    return  jsonify(ManagementDB.StatusElemt(NameProyect))

@app.route('/BorrarVMProyecto')
@app.route('/BorrarVMProyecto/<NameProyect>')
@app.route('/BorrarVMProyecto/<NameProyect>/<VMs>')
def deleteVMProyect(NameProyect='default', VMs=''):
    path = envConfig.VAGRANTPROJECT + NameProyect
    if ManagementDB.ReadElemt(NameProyect) == True:
        if VagrantGest.CheckVagrant(NameProyect):
            if VagrantGest.VmCreated(NameProyect)!='0':
            #1) Se destruyen maquinas
                VagrantGest.VagrantDestroy(NameProyect, VMs)
            #2) Actualizar DB
                ManagementDB.ModifyElemt(NameProyect, NameProyect, VagrantGest.VagrantStatus(NameProyect))
            #3) Respuesta
                return 'Del proyecto: ' + NameProyect + ' se elimino ' + VMs + '\n'
            else:
            #3) Respuesta
                return 'El proyecto: ' + NameProyect + ' no tiene VM creadas\n'
        else:
            return 'Existe en DB y pero no hay Vagrantfile\n'
    else:
        return 'No existe en DB\n'

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0",  port=8000)