import unittest
from unittest.mock import MagicMock, patch
from bson import ObjectId
from pymongo.cursor import Cursor
from perfil_funciones import conectar_db, obtener_dudas_usuario, borrar_duda_por_id, obtener_total_dudas_usuario, obtener_total_votos

class TestFunciones(unittest.TestCase):

    @patch('perfil_funciones.MongoClient')
    def test_conectar_db(self, mock_mongo_client):
        # Configura el comportamiento del mock
        mock_db = MagicMock()
        mock_form_collection = MagicMock()
        mock_mongo_client.return_value.__getitem__.side_effect = [mock_db, mock_form_collection]

        # Llama a la función que estás probando
        form_collection = conectar_db()

        # Realiza las aserciones necesarias
        mock_mongo_client.assert_called_once_with('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
        mock_db.__getitem__.assert_called_once_with('TFG')
        mock_form_collection.__getitem__.assert_called_once_with('publicar_duda')

        self.assertEqual(form_collection, mock_form_collection)



    @patch('perfil_funciones.conectar_db')
    def test_obtener_dudas_usuario(self, mock_conectar_db):
        # Configura los mocks
        mock_form_collection = MagicMock()
        mock_conectar_db.return_value = mock_form_collection

        # Configura el resultado simulado para find
        mock_cursor = MagicMock(spec=Cursor)
        mock_form_collection.find.return_value = mock_cursor

        # Ejecuta la función y verifica las llamadas a los mocks
        correo_usuario = "usuario@example.com"
        dudas = obtener_dudas_usuario(correo_usuario)

        mock_conectar_db.assert_called_once()
        mock_form_collection.find.assert_called_once_with({'correo_usuario': correo_usuario})
        self.assertEqual(dudas, mock_cursor)

    @patch('perfil_funciones.conectar_db')
    def test_borrar_duda_por_id(self, mock_conectar_db):
        # Configura los mocks
        mock_form_collection = MagicMock()
        mock_conectar_db.return_value = mock_form_collection

        # Configura el mock para el objeto de duda
        duda_id = str(ObjectId())
        mock_form_collection.find_one.return_value = {"_id": duda_id}

        # Ejecuta la función y verifica las llamadas a los mocks
        borrar_duda_por_id(duda_id)

        mock_conectar_db.assert_called_once()
        mock_form_collection.find_one.assert_called_once_with({'_id': ObjectId(duda_id)})
        mock_form_collection.delete_one.assert_called_once_with({'_id': ObjectId(duda_id)})

    @patch('perfil_funciones.conectar_db')
    def test_obtener_total_dudas_usuario(self, mock_conectar_db):
        # Configura los mocks
        mock_form_collection = MagicMock()
        mock_conectar_db.return_value = mock_form_collection

        # Configura el resultado simulado del conteo
        correo_usuario = "usuario@example.com"
        total_dudas_usuario = 42
        mock_form_collection.count_documents.return_value = total_dudas_usuario

        # Ejecuta la función y verifica las llamadas a los mocks
        resultado = obtener_total_dudas_usuario(correo_usuario)

        mock_conectar_db.assert_called_once()
        mock_form_collection.count_documents.assert_called_once_with({'correo_usuario': correo_usuario})
        self.assertEqual(resultado, total_dudas_usuario)

    @patch('perfil_funciones.comentarios_collection')
    @patch('perfil_funciones.conectar_db')
    def test_obtener_total_votos(self, mock_conectar_db, mock_comentarios_collection):
        # Configura los mocks
        mock_conectar_db.return_value = MagicMock()
        mock_comentarios_collection.find.return_value = MagicMock(spec=Cursor)

        # Configura el resultado simulado para los votos
        correo_usuario = "usuario@example.com"
        votos_positivos = 10
        votos_negativos = 5
        mock_cursor = mock_comentarios_collection.find.return_value
        mock_cursor.__iter__.return_value = [
            {"comentario": {"correo": correo_usuario, "votos_positivos": votos_positivos, "votos_negativos": votos_negativos}},
            {"comentario": {"correo": correo_usuario, "votos_positivos": votos_positivos, "votos_negativos": votos_negativos}},
        ]

        # Ejecuta la función y verifica las llamadas a los mocks
        total_votos_positivos, total_votos_negativos = obtener_total_votos(correo_usuario)

        mock_conectar_db.assert_called_once()
        mock_comentarios_collection.find.assert_called_once_with({'comentario.correo': correo_usuario})
        self.assertEqual(total_votos_positivos, 2 * votos_positivos)
        self.assertEqual(total_votos_negativos, 2 * votos_negativos)

if __name__ == '__main__':
    unittest.main()
