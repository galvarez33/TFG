from flask import render_template, session, redirect, url_for, Blueprint, flash, jsonify, request
from flask_mail import Mail
from pymongo import MongoClient
from flask_jwt import jwt

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




