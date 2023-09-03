from flask import render_template, request, redirect, session, url_for, Blueprint
from datetime import datetime
import base64
from pymongo import MongoClient
from . import publicar_duda_bp



# Conectar a la base de datos MongoDB (esto puede ir en tu archivo main.py)
client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
db = client['TFG']
form_collection = db['publicar_duda']

# Ruta para publicar una nueva duda
@publicar_duda_bp.route('/publicar_duda', methods=['GET', 'POST'])
def publicar_duda():
    logged_user = session.get('logged_user')
    if not logged_user:
        return redirect(url_for('auth.login'))  # Redirigir al inicio de sesión si el usuario no está autenticado

    if request.method == 'POST':
        imagen = request.files['imagen']
        titulo = request.form['titulo']
        texto = request.form['texto']
        carrera = request.form['carrera']
        curso = request.form['curso']
        asignatura = request.form['asignatura']
        dificultad = int(request.form['dificultad'])  # Convertir a entero

        if imagen:
            imagen_base64 = base64.b64encode(imagen.read()).decode('utf-8')
        else:
            imagen_base64 = None

        # Obtener el correo del usuario logueado desde la sesión
        usuario_correo = session['logged_user']['correo']

        # Guardar la información en la base de datos
        form_data = {
            'imagen': imagen_base64,
            'titulo': titulo,
            'texto': texto,
            'carrera': carrera,
            'curso': curso,
            'asignatura': asignatura,
            'dificultad': dificultad,
            'correo_usuario': usuario_correo,  # Agregar el correo del usuario
            'comentario': []
        }
        form_collection.insert_one(form_data)

        return redirect(url_for('explorar.explorar'))  # Redirigir a la página de exploración de dudas después de publicar

    return render_template('publicar_duda.html', logged_user=logged_user)


