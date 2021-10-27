from flask import Flask, render_template, url_for, redirect, request,session,flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import db
import sqlite3



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
        session.pop('usuario')
    return redirect(url_for('index'))

    
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method=='POST':
        nombre = request.form['nombre']
        usuario = request.form['usuario']
        correo = request.form['correo']
        clave = request.form['clave']
        clavehash = generate_password_hash(clave)
        db.registrar_usuario(nombre, usuario, correo, clavehash,rol=3)
        return render_template('login.html')
    else:
        return render_template('register.html')

@app.route('/usuarios', methods=['POST', 'GET'])
def usuario():
    with sqlite3.connect("restaurante.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM usuarios")
        usuarioscall =  cur.fetchall()
        return render_template('usuarios.html', usuarioscall=usuarioscall)
    

@app.route('/editUserCall', methods=['GET', 'POST'])
def editUserCall():
    print("-------------------------------------------")
    with sqlite3.connect("restaurante.db") as con:
        id = request.args.get('id')
        if request.method == 'GET':
            id = request.args.get('id')
            print(id)
            cur = con.cursor()
            cur.execute(f'SELECT * FROM usuarios WHERE id = {id}')        
            usercalled = cur.fetchall()[0]
            return render_template('editUserCall.html', usercalled=usercalled)
        if request.method == 'POST':
            id = request.args.get('id')
            print(id)
            cur = con.cursor()
            nombre = request.form['nombreED']
            correo = request.form['correoED']
            usuario = request.form['usuarioED']
            rol = request.form['rolED']
            cur.execute("UPDATE usuarios SET nombre = ?, correo = ?, usuario = ?, rol = ? WHERE id = ?",(nombre, correo, usuario, rol, id))  
            con.commit()
            print("hola")         
        return redirect(url_for('usuario'))



@app.route('/deleteUserCall', methods=['GET', 'POST'])
def deleteUserCall():
    with sqlite3.connect("restaurante.db") as con:
        id = request.args.get('id')
        print(id)
        cur = con.cursor()
        cur.execute(f'DELETE FROM usuarios WHERE id = {id}')     
        con.commit()
        return redirect(url_for('usuario'))




@app.route('/platos', methods=['POST', 'GET'])
def plato():
    db.mostrar_platos()
    return render_template('platos.html')


    
