import sqlite3
from flask import session
from werkzeug.security import check_password_hash


CONEXION = 'restaurante.db'


def registrar_usuario(nombre, usuario, correo, clave, rol):
    with sqlite3.connect(CONEXION) as con:
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
    with sqlite3.connect(CONEXION) as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM platos' )
        platos = cur.fetchall() 
        return platos


def agregar_plato(plato, descripcion, filename, precio):
    with sqlite3.connect(CONEXION) as con:
        cur = con.cursor()
        cur.execute('INSERT INTO platos (plato, descripcion, imagen, precio, id_disponiblidad) VALUES (?,?,?,?,?)', (plato, descripcion, filename, float(precio), 1)) 
        con.commit()


def eliminar_plato(id):
    with sqlite3.connect(CONEXION) as con:
        cur = con.cursor()
        cur.execute(f'DELETE FROM platos WHERE id ={id} ')
        con.commit()


def editar_plato(id,plato, descripcion, filename, precio):
    with sqlite3.connect(CONEXION) as con:
        cur = con.cursor()
        cur.execute(f'UPDATE platos SET plato=?, descripcion=?, imagen=?, precio=?, id_disponiblidad=? WHERE id={id}', (plato, descripcion, filename, precio,1))
        con.commit()


def cargar_plato(id):
    with sqlite3.connect(CONEXION) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM platos WHERE id = {id}")
        plato = cur.fetchall()[0]
        return plato