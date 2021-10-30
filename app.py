from flask import Flask, render_template, url_for, redirect, request,session,flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import db
import sqlite3



app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_IMAGE'] = "static/img-platos"


@app.route('/')
def index():
    with sqlite3.connect("restaurante.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM platos")
        platoslist = cur.fetchall()
        return render_template('index.html',PL=platoslist)




@app.route('/pedidos', methods=['POST', 'GET'])
def pedido():
    return render_template('pedido.html')
   
@app.route('/menu', methods=['POST', 'GET'])
def menu():
    with sqlite3.connect("restaurante.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM platos")
        platoslist = cur.fetchall()
        return render_template('menu.html',PL=platoslist)

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        busqueda = request.form['busqueda']
        with sqlite3.connect("restaurante.db") as con:
            cur = con.cursor()
            cur.execute(f'SELECT * FROM platos WHERE plato LIKE "%{busqueda}%"')
            platoslist = cur.fetchall()
            return render_template('menu.html',PL=platoslist)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        usuario = request.form['nombre2']
        clave = request.form['password2']
        with sqlite3.connect("restaurante.db") as con:
            cur = con.cursor()
            cur.execute(f'SELECT * FROM usuarios WHERE usuario = "{usuario}"')
            usuarios = cur.fetchall() 
            if len(usuarios) != 0:
                contraseñaHash = usuarios[0][4]
                if check_password_hash(contraseñaHash, clave):
                    session.clear()
                    session['id'] = usuarios[0][0]
                    session['nombre'] = usuarios[0][1]
                    session['correo'] = usuarios[0][2]
                    session['clave'] = contraseñaHash
                    session['usuario'] = usuarios[0][3]
                    session['rol'] = usuarios[0][5]
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
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route('/usuarios', methods=['POST', 'GET'])
def usuario():
    with sqlite3.connect("restaurante.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM usuarios")
        usuarioscall =  cur.fetchall()
        return render_template('usuarios.html', usuarioscall=usuarioscall)
    

@app.route('/editUserCall/<id>', methods=['GET', 'POST'])
def editUserCall(id):
    print("-------------------------------------------")
    with sqlite3.connect("restaurante.db") as con:
        if request.method == 'GET':
            cur = con.cursor()
            cur.execute(f"SELECT * FROM usuarios WHERE id = {id}")
            userlist = cur.fetchall()[0]
            return render_template('editUserCall.html',US=userlist)
        if request.method == 'POST':
            cur = con.cursor()
            nombre = request.form['nombreED']
            correo = request.form['correoED']
            usuario = request.form['usuarioED']
            rol = request.form['rolED']
            cur.execute(f"UPDATE usuarios SET nombre = ?, correo = ?, usuario = ?, rol = ? WHERE id = {id}",(nombre, correo, usuario, rol))  
            con.commit()
        return redirect(url_for('usuario'))


@app.route('/deleteUserCall', methods=['GET', 'POST'])
def deleteUserCall():
    with sqlite3.connect("restaurante.db") as con:
        id = request.args.get('id')
        cur = con.cursor()
        cur.execute(f'DELETE FROM usuarios WHERE id = {id}')     
        con.commit()
        return redirect(url_for('usuario'))




@app.route('/platos', methods=['POST', 'GET'])
def plato():
    platos = db.mostrar_platos()
    return render_template('platos.html', platos=platos)


@app.route('/platos/add', methods=['POST', 'GET'])
def agregar_platos():
    if request.method == 'POST':
        plato = request.form['plato']
        descripcion = request.form['descripcion']
        f = request.files['imagen']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_IMAGE'], filename))
        precio = float(request.form['precio'])
        db.agregar_plato(plato, descripcion, filename, precio )
        return redirect(url_for('plato'))
    else:
        return render_template('agregarPlato.html')

@app.route('/platos/eliminar/<id>')
def platos_eliminar(id):
    db.eliminar_plato(id)
    return redirect(url_for('plato'))


@app.route('/platos/editar/<id>', methods=['POST', 'GET'])
def editar_plato(id):
    if request.method == 'GET':
        return render_template('editarPlato.html')
    if request.method == 'POST':
        plato = request.form['plato']
        descripcion = request.form['descripcion']
        f = request.files['imagen']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_IMAGE'], filename))
        precio = float(request.form['precio'])
        db.editar_plato(id,plato,descripcion,filename,precio)
        return redirect(url_for('plato'))

    return render_template('editarPlato.html')


    
