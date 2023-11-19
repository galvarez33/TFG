from flask import render_template, session, redirect, url_for, Blueprint, flash, jsonify, request
from flask_mail import Mail, Message
from pymongo import MongoClient
<<<<<<< HEAD
import jwt
=======
from flask_jwt_extended import JWTManager
>>>>>>> 0ca327b2174889b2027bd171e3a834e5a56f55fd
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
                'nombre': user['nombre'],
                'nia': user['nia'], 
                'contraseña': user['contraseña'] 
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
        session['correo_usuario'] = credenciales['user_data']['correo']
        session['nia_usuario'] = credenciales['user_data']['nia'] 
        session['contraseña_usuario'] = credenciales['user_data']['contraseña']


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
    
    # Actualizar la contraseña en la base de datos
    resultado = collection.update_one({'correo': correo}, {'$set': {'contraseña': nueva_contrasena}})
    
    # Verificar si la actualización fue exitosa
    return resultado.modified_count > 0


def enviar_correo_restablecer_contrasena(correo, token):
    mail = Mail()

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
    

    #----------------------------------Funciones para cambiar contraseña cuando estas logeado---------------


def obtener_usuario_por_correo(db, correo):
    usuario = db.collection.find_one({'correo': correo})
    return usuario

def actualizar_contrasena(db, correo, nueva_contrasena):
    db.collection.update_one({'correo': correo}, {'$set': {'contraseña': nueva_contrasena}})

    