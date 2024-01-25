from flask import render_template, request, redirect, session, url_for, Blueprint, jsonify
from funciones.publicar_duda_funciones import guardar_nueva_duda
from ia.validacion import detectar_texto_en_imagen
from PIL import Image
import base64
import numpy as np
import io
import requests
from bson import Binary

from . import publicar_duda_bp


def save_file_to_mongodb(file):
    # Convert the FileStorage object to bytes and store in MongoDB
    return Binary(file.read())


@publicar_duda_bp.route('/publicar_duda', methods=['GET', 'POST'])
def publicar_duda():
    logged_user = session.get('logged_user')
    error_message = request.args.get('error', None)

    if not logged_user:
        return redirect(url_for('auth.login'))

    usuario_correo = session['logged_user']['correo']

    # Realizar una solicitud GET a la API de perfil para obtener la imagen de perfil
    perfil_api_url = f'http://localhost/api/perfil/{usuario_correo}'
    perfil_api_response = requests.get(perfil_api_url)

    

    if request.method == 'POST':
        if perfil_api_response.status_code == 200:
            imagen_perfil = perfil_api_response.json().get('imagen_perfil')
            
        

        imagen = request.files['imagen']
        titulo = request.form['titulo']
        texto = request.form['texto']
        carrera = request.form['carrera']
        curso = request.form['curso']
        asignatura = request.form['asignatura']
        dificultad = int(request.form['dificultad'])
        
        imagen_base64 = base64.b64encode(imagen.read()).decode('utf-8')
        
        form_data = {
            'imagen': imagen_base64,  # Assuming 'imagen' is the image file from the form
            'imagen_perfil': imagen_perfil,
            'titulo': titulo,
            'texto': texto,
            'carrera': carrera,
            'curso': curso,
            'asignatura': asignatura,
            'dificultad': dificultad,
            'correo_usuario': usuario_correo,
            'comentario': []
        }

        # Guardar la nueva duda en la base de datos usando la función
        duda_id = guardar_nueva_duda(form_data)
        return redirect(url_for('detalle_duda.detalle_duda_view', duda_id=duda_id))

    return render_template('publicar_duda.html', logged_user=logged_user, error=error_message)

# Ruta para la página con error
@publicar_duda_bp.route('/error-texto')
def pagina_con_error():
    logged_user = session.get('logged_user')
    error_message = request.args.get('error', 'Error desconocido')
    return render_template('publicar_duda.html', logged_user=logged_user, error=error_message)