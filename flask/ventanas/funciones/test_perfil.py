import unittest
from unittest.mock import MagicMock, patch
from bson import ObjectId
from pymongo.cursor import Cursor
from perfil_funciones import conectar_db, obtener_dudas_usuario, borrar_duda_por_id, obtener_total_dudas_usuario, obtener_total_votos

class TestFunciones(unittest.TestCase):

    @patch('perfil_funciones.MongoClient')
    def test_conectar_db(self, mock_mongo_client):
        mock_db = MagicMock()
        mock_form_collection = MagicMock()
        mock_mongo_client.return_value.__getitem__.side_effect = [mock_db, mock_form_collection]

        form_collection = conectar_db()

        mock_mongo_client.assert_called_once_with('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
        mock_db.__getitem__.assert_called_once_with('TFG')
        mock_form_collection.__getitem__.assert_called_once_with('publicar_duda')

        self.assertEqual(form_collection, mock_form_collection)

    @patch('perfil_funciones.obtener_dudas_usuario')
    def test_obtener_dudas_usuario(self, mock_obtener_dudas_usuario):
        mock_form_collection = MagicMock()
        mock_obtener_dudas_usuario.return_value = mock_form_collection.find.return_value

        correo_usuario = "usuario@example.com"
        dudas = obtener_dudas_usuario(correo_usuario)

        mock_obtener_dudas_usuario.assert_called_once_with(correo_usuario)
        mock_form_collection.find.assert_called_once_with({'correo_usuario': correo_usuario})
        self.assertEqual(dudas, mock_form_collection.find.return_value)

    @patch('perfil_funciones.borrar_duda_por_id')
    def test_borrar_duda_por_id(self, mock_borrar_duda_por_id):
        duda_id = str(ObjectId())
        borrar_duda_por_id(duda_id)

        mock_borrar_duda_por_id.assert_called_once_with(duda_id)

    @patch('perfil_funciones.obtener_total_dudas_usuario')
    def test_obtener_total_dudas_usuario(self, mock_obtener_total_dudas_usuario):
        mock_obtener_total_dudas_usuario.return_value = 42

        correo_usuario = "usuario@example.com"
        resultado = obtener_total_dudas_usuario(correo_usuario)

        mock_obtener_total_dudas_usuario.assert_called_once_with(correo_usuario)
        self.assertEqual(resultado, 42)

    @patch('perfil_funciones.obtener_total_votos')
    def test_obtener_total_votos(self, mock_obtener_total_votos):
        correo_usuario = "usuario@example.com"
        mock_obtener_total_votos.return_value = (10, 5)

        total_votos_positivos, total_votos_negativos = obtener_total_votos(correo_usuario)

        mock_obtener_total_votos.assert_called_once_with(correo_usuario)
        self.assertEqual(total_votos_positivos, 10)
        self.assertEqual(total_votos_negativos, 5)
