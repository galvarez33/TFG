
from flask import render_template, request, redirect, session, url_for, Blueprint
import requests
from operator import itemgetter

from funciones.detalle_duda_funciones import conectar_db, obtener_detalle_duda, votar_positivo_comentario, votar_negativo_comentario, borrar_comentario, agregar_comentario
from . import detalle_duda_bp
from datetime import datetime
import base64
from  ia.validacion import detectar_texto_en_imagen





@detalle_duda_bp.route('/detalle_duda/<string:duda_id>', methods=['GET', 'POST'])
def detalle_duda_view(duda_id):
    logged_user = session.get('logged_user')
    if not logged_user:
        return redirect(url_for('auth.login'))
    orden = request.args.get('orden')
    api_url = f'http://localhost:5001/api/detalle_duda/{duda_id}'
    api_response = requests.get(api_url)
    nombre_usuario = session.get('nombre_usuario')

    if request.method == 'POST':
        duda = api_response.json().get('duda')

        for comentario in duda['comentarios']:
            comentario['votos_positivos_count'] = comentario.get('votos_positivos', 0)

        correo_usuario = session.get('correo_usuario')
        nuevo_comentario = request.form.get('comentario')
        imagen = request.files.get('imagen')

        if imagen:
            imagen_base64 = base64.b64encode(imagen.read()).decode('utf-8')
            
            # Llamar a la función para detectar texto en la imagen
            tiene_texto = detectar_texto_en_imagen(imagen_base64)
            print(tiene_texto)
            if tiene_texto == False:
                # La imagen contiene texto, muestra el error
                return render_template('detalle_duda.html', duda=duda, logged_user=logged_user, nombre_usuario=session.get('nombre_usuario'), error="Debe seleccionar una imagen que contenga texto")
        else:
            imagen_base64 = None

        # Resto del código para agregar el comentario
        comentario_con_imagen = {
            'nombre': nombre_usuario,
            'correo': correo_usuario,
            'texto': nuevo_comentario,
            'imagen': imagen_base64,
            'votos_positivos': 0,
            'votos_negativos': 0,
            'fecha_agregado': datetime.now().isoformat() 
        }

        # Hacer la solicitud a la API para agregar el comentario
        api_agregar_comentario_url = f'http://localhost:5001/api/detalle_duda/{duda_id}'
        api_agregar_comentario_response = requests.post(api_agregar_comentario_url, json=comentario_con_imagen)

        if api_agregar_comentario_response.status_code == 201:
            return redirect(url_for('detalle_duda.detalle_duda_view', duda_id=duda['_id']))
        else:
            return render_template('error.html', mensaje='Error al agregar el comentario')



    


    if api_response.status_code == 200:
        duda = api_response.json().get('duda')
        comentarios = duda.get('comentarios', [])
        if orden == 'recientes':
            comentarios.sort(key=itemgetter('fecha_agregado'), reverse=True)
        
        elif orden == 'mejor_votados':
            comentarios.sort(key=itemgetter('votos_positivos'), reverse=True)

        for comentario in duda['comentarios']:
            comentario['votos_positivos_count'] = comentario.get('votos_positivos', 0)

        return render_template('detalle_duda.html', duda=duda, comentarios=comentarios, logged_user=logged_user, nombre_usuario=session.get('nombre_usuario'))
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


@detalle_duda_bp.route('/borrar_comentario/<string:duda_id>/<int:comentario_index>', methods=['POST'])
def borrar_comentario_view(duda_id, comentario_index):
    logged_user = session.get('logged_user')
    if not logged_user:
        return 'Acceso no autorizado'

    api_url = f'http://localhost:5001/api/detalle_duda/{duda_id}'

    data = {
    'comentario_index': comentario_index
    }
    response = requests.delete(api_url, data=data)
    if response.status_code == 200:
        return redirect(url_for('detalle_duda.detalle_duda_view', duda_id=duda_id))
    else:
        return 'Error al borrar el comentario'

