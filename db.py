import sqlite3
from flask import Flask, render_template, url_for, redirect, request,session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

def registrar_usuario(nombre, usuario, correo, clave, rol):
    with sqlite3.connect("restaurante.db") as con:
        cur = con.cursor()
        cur.execute('INSERT INTO usuarios(nombre,correo,usuario,clave,rol) VALUES (?,?,?,?,?)', (nombre, correo, usuario,clave,rol)) 
        con.commit()
        
def wthigo(usuario,clave):
    with sqlite3.connect("restaurante.db") as con:
        cur = con.cursor()
        cur.execute(f'SELECT * FROM usuarios WHERE nombre = "{usuario}"')
        usuarios = cur.fetchall() 
        print(usuarios)
        if len(usuarios) > 0:
            contraseñaHash = usuarios[0][4]
            if check_password_hash(contraseñaHash, clave):
                session.clear()
                session['id'] = usuarios[0][0]
                session['nombre'] = usuarios[0][1]
                session['correo'] = usuarios[0][2]
                session['clave'] = contraseñaHash
                session['usuario'] = usuarios[0][3]
                session['rol'] = usuarios[0][5]
                return redirect(url_for('index'))  

def check_password(hashed_clave, usuario_clave):
    return hashed_clave == hashlib.sha1(usuario_clave.encode()).hexdigest()

def validar_usuario(usuario, clave):
    flag = False
    with sqlite3.connect("restaurante.db") as con:
        cur = con.cursor()
        cur.execute("SELECT usuario, clave FROM usuarios")
        rows = cur.fetchall()
        for row in rows:
            db_usuario = row[3]
            db_clave = row[4]
            if db_usuario == usuario:
                flag = check_password(db_clave, clave)
    return flag