import sqlite3
import hashlib


def registrar_usuario(nombre, usuario, correo, clave):
    with sqlite3.connect("restaurante.db") as con:
        cur = con.cursor()
        cur.execute('INSERT INTO usuarios(id,nombre,correo,usuario,clave) VALUES (null,?,?,?,?)', (nombre, correo, usuario, hashlib.sha1(clave.encode()).hexdigest())) 
        con.commit()

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