import unittest
import pymongo
from explorar_funciones import obtener_dudas, obtener_parametros_dudas

class TestExplorarFunciones(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_obtener_dudas(self):
        consulta = "ejemplo"
        carrera = "Informática"
        curso = "2023"
        page = 1
        per_page = 10

        dudas, total_dudas = obtener_dudas(consulta, carrera, curso, page, per_page)
        
        self.assertIsInstance(dudas, pymongo.cursor.Cursor)
        self.assertIsInstance(total_dudas, int)

        

    def test_obtener_parametros_dudas(self):
        parametros_dudas = obtener_parametros_dudas()
        
        self.assertIsInstance(parametros_dudas, list)


    def test_obtener_dudas2(self):
        consulta = ""
        carrera = None
        curso = None
        page = 1
        per_page = 10

        dudas, total_dudas = obtener_dudas(consulta, carrera, curso, page, per_page)
        
        self.assertIsInstance(dudas, pymongo.cursor.Cursor)
        self.assertIsInstance(total_dudas, int)

        
        carrera = "Informática"
        curso = "2023"

        dudas, total_dudas = obtener_dudas(consulta, carrera, curso, page, per_page)
        
        self.assertIsInstance(dudas, pymongo.cursor.Cursor)
        self.assertIsInstance(total_dudas, int)

    def test_obtener_dudas_paginacion(self):
        consulta = ""
        carrera = None
        curso = None
        page = 2 
        per_page = 5  

        dudas, total_dudas = obtener_dudas(consulta, carrera, curso, page, per_page)
        
        self.assertIsInstance(dudas, pymongo.cursor.Cursor)
        self.assertIsInstance(total_dudas, int)

    def test_obtener_dudas_error_pagina_invalida(self):
        consulta = ""
        carrera = None
        curso = None
        page = -1
        per_page = 10

        with self.assertRaises(ValueError):
            obtener_dudas(consulta, carrera, curso, page, per_page)

    def test_obtener_dudas_error_per_page_invalido(self):
        consulta = ""
        carrera = None
        curso = None
        page = 1
        per_page = -5

        with self.assertRaises(ValueError):
            obtener_dudas(consulta, carrera, curso, page, per_page)

        

if __name__ == '__main__':
    unittest.main()
