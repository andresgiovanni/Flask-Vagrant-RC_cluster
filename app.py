#!/usr/bin/env python
import os
from flask import Flask, render_template, request, jsonify
from werkzeug import secure_filename
import MGdir
# instancia del objeto Flask
app = Flask(__name__)

@app.route('/crear', methods=['POST'])
@app.route('/crear/<ruta>', methods=['POST'])
def uploader(ruta='default'):
  path = '/home/cherno/vagrantproyect/' + ruta
  if request.method == 'POST':
    if MGdir.CheckDB(path) == True:
      return 'Existe el proyeto: ' + ruta + '\n'
    else:
      MGdir.CreateProyect(path)
      f = request.files['file']
      filename = secure_filename(f.filename)
      f.save(os.path.join(path, filename))
      return 'Se creo proyecto: ' + ruta + '\n'

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0",  port=8000)