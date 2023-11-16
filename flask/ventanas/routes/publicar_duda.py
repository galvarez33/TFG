from flask import render_template, request, redirect, session, url_for, Blueprint, jsonify
from funciones.publicar_duda_funciones import guardar_nueva_duda
from ia.validacion import detectar_texto_en_imagen
from PIL import Image
import base64
import numpy as np
import io

from . import publicar_duda_bp

@publicar_duda_bp.route('/publicar_duda', methods=['GET', 'POST'])
def publicar_duda():
    logged_user = session.get('logged_user')
    imagen_base64 = None  # Inicializar con un valor predeterminado

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
            try:
                imagen_bytes = base64.b64decode(imagen.read())
                img = Image.open(io.BytesIO(imagen_bytes))
                print("Imagen abierta con éxito.")

                # Verificar si la imagen contiene texto
                if not detectar_texto_en_imagen(base64.b64encode(imagen_bytes).decode('utf-8')):
                    # La imagen no tiene texto, mostrar mensaje de error
                    error = "La imagen no contiene texto. Por favor, sube una imagen con texto."
                    return render_template('publicar_duda.html', logged_user=logged_user, error=error)

                
                
                # Actualizar imagen_base64 si es necesario
                imagen_base64 = base64.b64encode(imagen_bytes).decode('utf-8')
            except Exception as e:
                print(f"Error al procesar la imagen: {e}")
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

        

    return render_template('publicar_duda.html', logged_user=logged_user)
