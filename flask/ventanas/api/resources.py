# resources.py
from flask_restful import Resource

class HomeResource(Resource):
    def get(self):
        try:
        # Lógica para manejar la solicitud GET a /home y devolver una respuesta JSON
            return {
                "message": "Bienvenido al Foro de Estudiantes del CEU",
                "description": "Este es un espacio exclusivo para estudiantes del CEU donde puedes compartir tus conocimientos, resolver dudas y colaborar con tus compañeros en la comunidad académica.",
                "instructions": "Aprovecha al máximo esta plataforma para aprender y crecer juntos."
            }, 200
        except Exception as e:
            # En caso de un fallo, devuelve una respuesta de error personalizada
            return {
                "error": "Se produjo un error al procesar la solicitud",
                "details": str(e)
            }, 500
