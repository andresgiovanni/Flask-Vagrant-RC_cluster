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

@app.route('/BorrarProyecto')
@app.route('/BorrarProyecto/<NameProyect>')
@app.route('/BorrarProyecto/<NameProyect>/<VMs>')
def deleteProyect(NameProyect='default', VMs=''):
    path = envConfig.VAGRANTPROJECT + NameProyect
    return VagrantGest.VmNotCreates(NameProyect)
    if ManagementDB.ReadElemt(NameProyect) == True:
        if VagrantGest.CheckVagrant(NameProyect):
            #1) Se destruyen maquinas
            #if VagrantGest.VmNotCreates != '0':
            #    return "no hay creadas"
                #VagrantGest.VagrantDestroy(NameProyect, VMs)
                #rmtree(path)
                #ManagementDB.DeleteElemt(NameProyect)
            #else:
            #2) Se elimina folder
                #rmtree(path)
            #3) Se actualiza la DB
                #ManagementDB.DeleteElemt(NameProyect)
            return 'Existe en DB y Vagrantfile\n'
        else:
            return 'Existe en DB y pero no hay Vagrantfile\n'
    else:
        return 'No existe en DB\n'

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0",  port=8000)