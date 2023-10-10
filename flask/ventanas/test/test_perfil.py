import pytest
import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from funciones.perfil_funciones import obtener_dudas_usuario, form_collection

@pytest.fixture
def form_collection_mock():
    # Crear una versión simulada de la colección de MongoDB
    class FormCollectionMock:
        def __init__(self):
            self.data = []

        def insert_one(self, document):
            self.data.append(document)

        def find(self, query):
            # Simular la búsqueda en la base de datos
            return self.data

    # Reemplazar la colección real con la versión simulada
    form_collection._collection = FormCollectionMock()
    return form_collection

def test_obtener_dudas_usuario(form_collection_mock):
    usuario_prueba = "usuario@example.com"
    dudas_prueba = [
        {"correo_usuario": usuario_prueba, "texto": "Duda 1"},
        {"correo_usuario": usuario_prueba, "texto": "Duda 2"},
    ]
    for duda in dudas_prueba:
        form_collection_mock.insert_one(duda)

    correo_usuario = usuario_prueba
    page = 1
    per_page = 2 

    dudas_cursor = obtener_dudas_usuario(correo_usuario, page, per_page)
    dudas_lista = list(dudas_cursor) 
    assert len(dudas_lista) == 2 
