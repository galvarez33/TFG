import pytest
import sys,os
from bson import ObjectId
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from funciones.detalle_duda_funciones import (
    obtener_detalle_duda,
    agregar_comentario,
    votar_positivo_comentario,
    votar_negativo_comentario,
    borrar_comentario
)

@pytest.fixture
def form_collection_mock():
    return {
        'find_one': lambda query: {
            '_id': 'duda_id',
            'correo': 'usuario@example.com',
            'asignatura': 'Matemáticas',
            'comentario': []
        },
        'update_one': lambda query, update: True
    }

def test_obtener_detalle_duda(form_collection_mock):
    duda_id = ObjectId()  
    form_collection_mock['find_one'] = lambda query: {
        '_id': duda_id,
        'campo_ejemplo': 'valor_ejemplo' 
    }

    duda = obtener_detalle_duda(str(duda_id))

    assert duda is not None
    assert isinstance(duda, dict)

    assert '_id' in duda
    assert duda['_id'] == duda_id

    
    assert 'campo_ejemplo' in duda
    assert duda['campo_ejemplo'] == 'valor_ejemplo'

def test_agregar_comentario(form_collection_mock):
    duda_id = ObjectId()
    comentario = {
        'nombre': 'Usuario',
        'texto': 'Este es un comentario',
        'imagen_data': None
    }
    resultado = agregar_comentario(str(duda_id), comentario)
    assert resultado is True  

def test_votar_positivo_comentario(form_collection_mock):
    duda_id = ObjectId()  
    comentario_index = 0
    usuario_voto = 'usuario1'
    votar_positivo_comentario(str(duda_id), comentario_index, usuario_voto)

    
def test_votar_negativo_comentario(form_collection_mock):
    duda_id = ObjectId()  
    comentario_index = 0
    usuario_voto = 'usuario1'
    votar_negativo_comentario(str(duda_id), comentario_index, usuario_voto)  

    # ...
def test_borrar_comentario(form_collection_mock):
    duda_id = ObjectId()
    comentario_index = 0
    resultado = borrar_comentario(str(duda_id), comentario_index)
    assert resultado is True