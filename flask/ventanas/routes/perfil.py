from flask import render_template, request, redirect, session, url_for, Blueprint
from flask_paginate import Pagination, get_page_args
from . import perfil_bp
from funciones.perfil_funciones import obtener_dudas_usuario, obtener_total_dudas_usuario, borrar_duda_por_id

@perfil_bp.route('/perfil', methods=['GET', 'POST'])
def perfil():
    logged_user = session.get('logged_user')
    if not logged_user:
        return 'Acceso no autorizado'
    usuario_correo = logged_user['correo']

    if request.method == 'POST':
        consulta = request.form.get('consulta', '')
        carrera = request.form.get('carrera', '')
        curso = request.form.get('curso', '')

        dudas_usuario = obtener_dudas_usuario(usuario_correo)
    else:
        dudas_usuario = obtener_dudas_usuario(usuario_correo)

    # Obtener el número de página actual y la cantidad de elementos por página
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    per_page = 9  # Mostrar 9 elementos por página

    # Calcular el desplazamiento para la consulta en la base de datos
    offset = (page - 1) * per_page
    dudas_usuario = dudas_usuario.skip(offset).limit(per_page)
    total_dudas_usuario = obtener_total_dudas_usuario(usuario_correo)

    # Crear el objeto de paginación
    pagination = Pagination(page=page, per_page=per_page, total=total_dudas_usuario, css_framework='bootstrap4')
    return render_template('perfil.html', dudas=dudas_usuario, pagination=pagination, logged_user=logged_user)



@perfil_bp.route('/borrar_duda/<string:duda_id>', methods=['POST'])
def borrar_duda(duda_id):
    logged_user = session.get('logged_user')
    if not logged_user:
        return 'Acceso no autorizado'

    # Llamamos a la función existente para borrar la duda por su ID
    borrar_duda_por_id(duda_id)
    return redirect(url_for('perfil.perfil'))
