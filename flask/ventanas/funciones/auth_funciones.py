from flask import render_template, session, redirect, url_for, Blueprint, flash, jsonify, request
from flask_mail import Mail, Message
from pymongo import MongoClient
from flask_jwt import jwt
from itsdangerous import URLSafeTimedSerializer
import re




# Configura la conexión a la base de datos MongoDB
def conectar_bd():
    client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
    db = client['TFG']  # Reemplaza 'TFG' por el nombre de tu base de datos
    return db

collection = conectar_bd()['usuarios']  # Conexión a la colección 'usuarios'
mail = Mail()
secret_key = '12345'
#----------------------------------------Inicio de sesion------------------------------------------------------#

def verificar_credenciales(username, password):
    user = collection.find_one({'correo': username, 'contraseña': password})
    if user:
        return {
            'access_token': jwt.encode({'identity': user['correo']}, secret_key),
            'user_data': {
                'correo': user['correo'],
                'nombre': user['nombre']
            }
        }
    else:
        return None

def iniciar_sesion(username, password):
    credenciales = verificar_credenciales(username, password)
    if credenciales:
        session['access_token'] = credenciales['access_token']
        session['logged_user'] = credenciales['user_data']
        session['nombre_usuario'] = credenciales['user_data']['nombre']
        return True
    return False

def usuario_ya_autenticado():
    return 'logged_user' in session

def cerrar_sesion():
    session.clear()


#--------------------------------Registro-------------------------------------------------------------#



def generar_token(correo):
    serializer = URLSafeTimedSerializer(secret_key)
    token = serializer.dumps({'correo': correo}, salt='restablecer-contrasena')
    return token

def obtener_correo_desde_token(token):
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        data = serializer.loads(token, salt='restablecer-contrasena', max_age=3600)
        correo = data['correo']
        return correo
    except:
        return None

def enviar_correo_verificacion(correo, contraseña, nia, nombre):
    token = generar_token(correo)
    url_verificacion = url_for('auth.confirmar_correo', token=token, contraseña=contraseña, nia=nia, nombre=nombre, _external=True)

    mensaje = Message('Verificación de correo electrónico', sender='ceupractica@gmail.com', recipients=[correo])
    mensaje.body = f'Haz clic en el siguiente enlace para verificar tu correo electrónico: {url_verificacion}'

    mail.send(mensaje)

def confirmar_correo_en_bd(correo, contraseña, nia, nombre):
    datos_usuario = {
        'correo': correo,
        'contraseña': contraseña,
        'nia': nia,
        'nombre': nombre
    }

    db = conectar_bd()
    collection = db['usuarios']
    collection.insert_one(datos_usuario)

def verificar_credenciales_en_bd(username, password):
    db = conectar_bd()
    collection = db['usuarios']
    user = collection.find_one({'correo': username, 'contraseña': password})
    return user


