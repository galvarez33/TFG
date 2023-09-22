from flask import render_template, request, redirect, session, url_for, Blueprint
from datetime import datetime
import base64
from . import publicar_duda_bp
from funciones.publicar_duda_funciones import guardar_nueva_duda

@publicar_duda_bp.route('/publicar_duda', methods=['GET', 'POST'])
def publicar_duda():
    logged_user = session.get('logged_user')
    if not logged_user:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        # Obtener datos del formulario
        imagen = request.files['imagen']
        titulo = request.form['titulo']
        texto = request.form['texto']
        carrera = request.form['carrera']
        curso = request.form['curso']
        asignatura = request.form['asignatura']
        dificultad = int(request.form['dificultad'])

        if imagen:
            imagen_base64 = base64.b64encode(imagen.read()).decode('utf-8')
        else:
            imagen_base64 = None

        usuario_correo = session['logged_user']['correo']

        # Crear el objeto de datos para la nueva duda
        form_data = {
            'imagen': imagen_base64,
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
        guardar_nueva_duda(form_data)

        return redirect(url_for('explorar.explorar'))

    return render_template('publicar_duda.html', logged_user=logged_user)

# Otras rutas y funciones de vistas pueden ir aquí.
