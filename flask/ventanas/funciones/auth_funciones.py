from flask import render_template, session, redirect, url_for, Blueprint, flash, jsonify, request
from flask_mail import Mail, Message
from pymongo import MongoClient
import jwt
from itsdangerous import URLSafeTimedSerializer
import re
import base64
import hashlib
from urllib.parse import unquote,quote_plus,quote

# -*- coding: utf-8 -*-



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
    hashed_password = hash_password(password)
    credenciales = verificar_credenciales(username, hashed_password)
    
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

def hash_password(password):
    # Usar SHA-256 para hashear la contraseña
    hashed_password = hashlib.sha256(password.encode()).digest()

    # Codificar el hash resultante con base64 y manejar el padding adecuadamente
    encoded_password = base64.urlsafe_b64encode(hashed_password + b'\x00').decode('utf-8', errors='replace').rstrip("=")

    return encoded_password

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

def enviar_correo_verificacion(correo, contrasena, nia, nombre,token):
    mail = Mail()  
   
    contrasena_hashed = hash_password(contrasena)
    url_restablecer = url_for('auth.confirmar_correo', contrasena=contrasena_hashed, nia=nia, nombre=nombre, correo=correo, token=token, _external=True)

    
    mensaje = Message('Confirmar correo', sender='tu_correo@gmail.com', recipients=[correo])
    mensaje.body = f'Haz clic en el siguiente enlace para restablecer tu contraseña: {url_restablecer}'

    try:
        mail.send(mensaje)  
        return True
    except Exception as e:
        print(f"Error al enviar el correo de restablecimiento de contraseña: {str(e)}")
        return False
    

def confirmar_correo_en_bd(correo, contrasena, nia, nombre):
    
    datos_usuario = {
        'correo': correo,
        'contraseña': contrasena,
        'nia': nia,
        'nombre': nombre
    }

    db = conectar_bd()
    collection = db['usuarios']
    collection.insert_one(datos_usuario)

def verificar_credenciales_en_bd(username, password):
    
    db = conectar_bd()
    collection = db['usuarios']
    user = collection.find_one({'correo': username})
    
    return user



#----------------------------------------Funciones para restablecer contraseña---------------------------

# Verificar si un usuario existe en la base de datos por su correo
def verificar_usuario_por_correo(correo):
    db = conectar_bd()
    collection = db['usuarios']
    usuario = collection.find_one({'correo': correo})
    return usuario is not None 

# Actualizar la contraseña de un usuario en la base de datos
def actualizar_contrasena_en_bd(correo, nueva_contrasena):
    db = conectar_bd()
    collection = db['usuarios']
    print(correo)
    correo=correo.replace('*40', '@')
    # Actualizar la contraseña en la base de datos
    resultado = collection.update_one({'correo': correo}, {'$set': {'contraseña': hash_password(nueva_contrasena)}})
    
    # Verificar si la actualización fue exitosa
    return resultado.modified_count > 0


def enviar_correo_restablecer_contrasena(correo, token):
    mail = Mail()  # Asegúrate de haber configurado la extensión Mail en tu aplicación Flask
    # Genera la URL para restablecer la contraseña
    url_restablecer = url_for('auth.restablecer_contrasena', correo=correo, token=token, _external=True)
    mensaje = Message('Restablecer contraseña', sender='tu_correo@gmail.com', recipients=[correo])
    mensaje.body = f'Haz clic en el siguiente enlace para restablecer tu contraseña: {url_restablecer}'
   

    try:
        mail.send(mensaje)  # Envía el correo
        return True
    except Exception as e:
        print(f"Error al enviar el correo de restablecimiento de contraseña: {str(e)}")
        return False