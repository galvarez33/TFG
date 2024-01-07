import pytest
import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from funciones.perfil_funciones import obtener_dudas_usuario, form_collection, borrar_duda_por_id, obtener_total_dudas_usuario,obtener_total_votos
from bson import ObjectId
from unittest.mock import Mock



@pytest.fixture
def form_collection_mock():
    # Crear una versión simulada de la colección de MongoDB
    class FormCollectionMock:
        def __init__(self):
            self.data = []

        def insert_one(self, document):
            self.data.append(document)

        def find(self, query):
            return self.data
    form_collection._collection = FormCollectionMock()
    return form_collection


def test_borrar_duda_por_id(form_collection_mock):
    duda_id_prueba = ObjectId() 
    
    duda_prueba = {
        "_id": duda_id_prueba,
        "correo_usuario": "usuario@example.com",
        "texto": "Esta es una duda de prueba"
    }
    form_collection_mock.insert_one(duda_prueba)

    borrar_duda_por_id(str(duda_id_prueba),"usuario@example.com")  # Convierte el ID en una cadena para asegurar la coincidencia

    duda_eliminada = form_collection_mock.find_one({"_id": duda_id_prueba})
    assert duda_eliminada is None  

def test_obtener_total_dudas_usuario(form_collection_mock):
    correos_prueba = ["usuario1@example.com", "usuario2@example.com"]
    for correo in correos_prueba:
        form_collection_mock.insert_one({"correo_usuario": correo, "texto": "Duda de prueba"})

    correo_usuario_prueba = "usuario1@example.com"
    total_dudas = obtener_total_dudas_usuario(correo_usuario_prueba)

    assert total_dudas == form_collection_mock.count_documents({"correo_usuario": correo_usuario_prueba})
    for correo in correos_prueba:
        form_collection_mock.delete_one({"correo_usuario": correo, "texto": "Duda de prueba"})


