from flask import Blueprint, render_template, session,request
from . import home_bp 
import requests

@home_bp.route('/')
def home():
    logged_user = session.get('logged_user')
    return render_template('home.html', logged_user=logged_user)

@home_bp.route('/notificacion', methods=['GET'])
def notificacion():
   logged_user = session.get('logged_user')
   correo_usuario = logged_user['correo']
   print(correo_usuario)
   api_url = f'https://practica-con-estudiantes-ceu.online/api/comentarios/{correo_usuario}'
   api_response = requests.get(api_url)
   


