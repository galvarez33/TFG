import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import pymongo
from funciones.explorar_funciones import obtener_dudas, obtener_parametros_dudas

def test_obtener_dudas():
    consulta = "ejemplo"
    carrera = "Informática"
    curso = "2023"
    page = 1
    per_page = 10

    dudas, total_dudas = obtener_dudas(consulta, carrera, curso, page, per_page)

    assert isinstance(dudas, pymongo.cursor.Cursor)
    assert isinstance(total_dudas, int)

def test_obtener_parametros_dudas():
    parametros_dudas = obtener_parametros_dudas()

    assert isinstance(parametros_dudas, list)

def test_obtener_dudas2():
    consulta = ""
    carrera = None
    curso = None
    page = 1
    per_page = 10

    dudas, total_dudas = obtener_dudas(consulta, carrera, curso, page, per_page)

    assert isinstance(dudas, pymongo.cursor.Cursor)
    assert isinstance(total_dudas, int)

    carrera = "Informática"
    curso = "2023"

    dudas, total_dudas = obtener_dudas(consulta, carrera, curso, page, per_page)

    assert isinstance(dudas, pymongo.cursor.Cursor)
    assert isinstance(total_dudas, int)

def test_obtener_dudas_paginacion():
    consulta = ""
    carrera = None
    curso = None
    page = 2
    per_page = 5

    dudas, total_dudas = obtener_dudas(consulta, carrera, curso, page, per_page)

    assert isinstance(dudas, pymongo.cursor.Cursor)
    assert isinstance(total_dudas, int)

def test_obtener_dudas_error_pagina_invalida():
    consulta = ""
    carrera = None
    curso = None
    page = -1
    per_page = 10

    with pytest.raises(ValueError):
        obtener_dudas(consulta, carrera, curso, page, per_page)

def test_obtener_dudas_error_per_page_invalido():
    consulta = ""
    carrera = None
    curso = None
    page = 1
    per_page = -5

    with pytest.raises(ValueError):
        obtener_dudas(consulta, carrera, curso, page, per_page)
