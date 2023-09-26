# En tu vista perfil

from flask import render_template, request, redirect, session, url_for, Blueprint
from flask_paginate import Pagination, get_page_args
from . import perfil_bp
from funciones.perfil_funciones import obtener_dudas_usuario, obtener_total_dudas_usuario, borrar_duda_por_id, obtener_total_votos

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

        page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
        per_page = 9  # Mostrar 9 elementos por página

        dudas_usuario = obtener_dudas_usuario(usuario_correo, page, per_page)
        
        total_votos_positivos, total_votos_negativos = obtener_total_votos(usuario_correo)  # Cambia a obtener_total_votos para obtener ambos valores
    else:
        dudas_usuario = obtener_dudas_usuario(usuario_correo)
        
        total_votos_positivos, total_votos_negativos = obtener_total_votos(usuario_correo)  # Cambia a obtener_total_votos para obtener ambos valores

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    per_page = 9  

    offset = (page - 1) * per_page
    dudas_usuario = dudas_usuario.skip(offset).limit(per_page)
    total_dudas_usuario = obtener_total_dudas_usuario(usuario_correo)

    pagination = Pagination(page=page, per_page=per_page, total=total_dudas_usuario, css_framework='bootstrap4')
    
    return render_template('perfil.html', dudas=dudas_usuario, pagination=pagination, logged_user=logged_user, total_votos_positivos=total_votos_positivos, total_votos_negativos=total_votos_negativos)  # Pasa ambos valores a la plantilla



@perfil_bp.route('/borrar_duda/<string:duda_id>', methods=['POST'])
def borrar_duda(duda_id):
    logged_user = session.get('logged_user')
    if not logged_user:
        return 'Acceso no autorizado'

    borrar_duda_por_id(duda_id)
    return redirect(url_for('perfil.perfil'))
