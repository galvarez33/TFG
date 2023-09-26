
from flask import render_template, request, redirect, session, url_for, Blueprint
from funciones.detalle_duda_funciones import conectar_db, obtener_detalle_duda, votar_positivo_comentario, votar_negativo_comentario, borrar_comentario, agregar_comentario
from . import detalle_duda_bp
from datetime import datetime
import base64


@detalle_duda_bp.route('/detalle_duda/<duda_id>', methods=['GET', 'POST'])
def detalle_duda_view(duda_id):
    logged_user = session.get('logged_user')
    if not logged_user:
        return redirect(url_for('auth.login'))  # Redirigir al inicio de sesión si el usuario no está autenticado

    nombre_usuario = session.get('nombre_usuario')

    duda = obtener_detalle_duda(duda_id)

    if duda:
        for comentario in duda['comentario']:
            comentario['votos_positivos_count'] = comentario.get('votos_positivos', 0)

        if request.method == 'POST':
            correo_usuario = session.get('correo_usuario')

            nuevo_comentario = request.form.get('comentario')
            imagen = request.files['imagen']

            if imagen:
                imagen_base64 = base64.b64encode(imagen.read()).decode('utf-8')
            else:
                imagen_base64 = None

            # Crear la tupla de comentario e imagen
            comentario_con_imagen = {
                'nombre': nombre_usuario,
                'correo': correo_usuario,
                'texto': nuevo_comentario,
                'imagen': imagen_base64,
                'votos_positivos': 0,
                'votos_negativos': 0,
                'fecha_agregado': datetime.now()  
            }

            resultado = agregar_comentario(duda, comentario_con_imagen)

            if resultado:
                return redirect(url_for('detalle_duda.detalle_duda_view', duda_id=duda['_id']))
            else:
                return render_template('error.html', mensaje='Error al agregar el comentario')

        comentario_index = request.args.get('comentario_index')
        if comentario_index is not None:
            comentario_index = int(comentario_index)
            resultado = borrar_comentario(duda['_id'], comentario_index)
            if resultado:
                return redirect(url_for('detalle_duda.detalle_duda_view', duda_id=duda['_id']))
            else:
                return render_template('error.html', mensaje='Error al borrar el comentario')

        orden = request.args.get('orden')
        if orden == 'mejor_votados':
            duda['comentario'].sort(key=lambda x: x['votos_positivos'], reverse=True)
        elif orden == 'recientes':
            duda['comentario'].sort(key=lambda x: x['fecha_agregado'], reverse=True)

        return render_template('detalle_duda.html', duda=duda, logged_user=logged_user, nombre_usuario=nombre_usuario)
    else:
        return render_template('error.html', mensaje='Duda no encontrada')


@detalle_duda_bp.route('/votar_positivo/<string:duda_id>/<int:comentario_index>', methods=['POST'])
def votar_positivo_view(duda_id, comentario_index):
    logged_user = session.get('logged_user')
    if not logged_user:
        return 'Acceso no autorizado'

    nombre_usuario = session.get('nombre_usuario')

    votar_positivo_comentario(duda_id, comentario_index, nombre_usuario)

    return redirect(url_for('detalle_duda.detalle_duda_view', duda_id=duda_id))

@detalle_duda_bp.route('/votar_negativo/<string:duda_id>/<int:comentario_index>', methods=['POST'])
def votar_negativo_view(duda_id, comentario_index):
    logged_user = session.get('logged_user')
    if not logged_user:
        return 'Acceso no autorizado'

    nombre_usuario = session.get('nombre_usuario')

    votar_negativo_comentario(duda_id, comentario_index, nombre_usuario)

    return redirect(url_for('detalle_duda.detalle_duda_view', duda_id=duda_id))

@detalle_duda_bp.route('/borrar_comentario/<duda_id>/<int:comentario_index>', methods=['POST'])
def borrar_comentario_view(duda_id, comentario_index):
    logged_user = session.get('logged_user')
    if not logged_user:
        return 'Acceso no autorizado'

    borrar_comentario(duda_id, comentario_index)

    return redirect(url_for('detalle_duda.detalle_duda_view', duda_id=duda_id))
