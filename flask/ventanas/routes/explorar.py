from flask import render_template, request, redirect, session, url_for, Blueprint
from pymongo import MongoClient
from flask_paginate import Pagination, get_page_parameter, get_page_args
from . import explorar_bp
from flasgger import Swagger, swag_from
from funciones.explorar_funciones import obtener_dudas
import requests



@explorar_bp.route('/explorar', methods=['GET', 'POST'])
def explorar():
    logged_user = session.get('logged_user')

    if request.method == 'POST':
        consulta = request.form.get('consulta', '')
        carrera = request.form.get('carrera', '')
        curso = request.form.get('curso', '')
        imagen = request.form.get('imagen', '')  
        api_url = 'https://practica-con-estudiantes-ceu.online/api/explorar' 

        response = requests.post(api_url, json={'consulta': consulta, 'carrera': carrera, 'curso': curso, 'imagen': imagen})
        data = response.json()
        dudas = data.get('dudas', [])

        
        response_all = requests.get(api_url)
        data_all = response_all.json().get('dudas', [])

        page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
        per_page = 9 
        start = (page - 1) * per_page
        end = start + per_page

        dudas_paginadas = dudas[start:end]
        total_dudas = len(dudas) 

        pagination = Pagination(page=page, per_page=per_page, total=total_dudas, css_framework='bootstrap4')

        return render_template('explorar.html', dudas=dudas_paginadas, pagination=pagination, logged_user=logged_user)



    api_url = 'https://practica-con-estudiantes-ceu.online/api/explorar' 
    response = requests.get(api_url)
    data = response.json().get('dudas', [])


    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    per_page = 9 
    start = (page - 1) * per_page
    end = start + per_page

    dudas = data[start:end]
    total_dudas = len(data)

    pagination = Pagination(page=page, per_page=per_page, total=total_dudas, css_framework='bootstrap4')

    return render_template('explorar.html', dudas=dudas, pagination=pagination, logged_user=logged_user)
