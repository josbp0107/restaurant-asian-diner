from flask import Flask
from flask import request
from flask import render_template
import db


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        nombre = request.form['nombre']
        usuario = request.form['usuario']
        correo = request.form['correo']
        clave = request.form['clave']
        db.registrar_usuario(nombre, usuario, correo, clave,rol=3)
        return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/pedidos', methods=['POST', 'GET'])
def pedido():
    
    pass
    
