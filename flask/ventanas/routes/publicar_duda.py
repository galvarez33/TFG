from flask import render_template, request, redirect, session, url_for, Blueprint, jsonify
from funciones.publicar_duda_funciones import guardar_nueva_duda
from ia.validacion import detectar_texto_en_imagen

publicar_duda_bp = Blueprint('publicar_duda', __name__)

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
            if not detectar_texto_en_imagen(imagen_base64):
                # La imagen no tiene texto, mostrar mensaje de error
                error = "La imagen no contiene texto. Por favor, sube una imagen con texto."
                return render_template('publicar_duda.html', logged_user=logged_user, error=error)

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

        # Enviar una respuesta JSON con los resultados obtenidos del modelo de IA
        # (carrera, curso y asignatura)
        asignatura_predicha = obtener_prediccion_asignatura(imagen_base64)
        return jsonify({
            'carrera': asignatura_predicha['carrera'],
            'curso': asignatura_predicha['curso'],
            'asignatura': asignatura_predicha['asignatura']
        })

    return render_template('publicar_duda.html', logged_user=logged_user)
