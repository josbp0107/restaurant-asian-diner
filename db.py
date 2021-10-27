import sqlite3
from flask import Flask, render_template, url_for, redirect, request,session,flash
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
        cur.execute(f'SELECT * FROM usuarios WHERE usuario = "{usuario}"')
        usuarios = cur.fetchall() 
        print(len(usuarios))
        print(usuarios)
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
            return True


def mostrar_platos():
    with sqlite3.connect("restaurante.db") as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM platos' )
        platos = cur.fetchall() 
        return platos

def eliminar_plato():
    with sqlite3.connect("restaurante.db") as con:
        cur = con.cursor()
        cur.execute('DELETE * FROM platos WHERE id = ?' (id) )
        
            
 

















""" def check_password(hashed_clave, usuario_clave):
    return hashed_clave == hashlib.sha1(usuario_clave.encode()).hexdigest() """




