from flask import Flask, render_template, url_for, redirect, request,session,flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import db


app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')





@app.route('/pedidos', methods=['POST', 'GET'])
def pedido():
    return render_template('pedido.html')
   
@app.route('/menu', methods=['POST', 'GET'])
def menu():
    return render_template('menu.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        usuario = request.form['nombre2']
        clave = request.form['password2']
        
        if db.wthigo(usuario, clave) == True:
            return render_template('index.html')
        else:
            return render_template('login.html')
            
    else:
        return render_template('login.html')
    
@app.route('/logout')
def logout():
    if 'usuario' in session:
        session.pop('user')
    return redirect(url_for('menu'))

    
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method=='POST':
        nombre = request.form['nombre']
        usuario = request.form['usuario']
        correo = request.form['correo']
        clave = request.form['clave']
        clavehash = generate_password_hash(clave)
        db.registrar_usuario(nombre, usuario, correo, clavehash,rol=3)
        return render_template('index.html')
    else:
        return render_template('register.html')

@app.route('/usuarios', methods=['POST', 'GET'])
def usuario():
    return render_template('usuarios.html')


@app.route('/platos', methods=['POST', 'GET'])
def plato():
    return render_template('platos.html')


    
