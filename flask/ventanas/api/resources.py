from flask_restful import Resource,reqparse
from flask import jsonify,session, Response, request
from datetime import datetime
import json
import io 
from PIL import Image
from bson import ObjectId
import joblib
import pytesseract

from funciones.explorar_funciones import obtener_parametros_dudas, obtener_dudas
from funciones.perfil_funciones import obtener_dudas_usuario,borrar_duda_por_id, obtener_total_votos
from funciones.detalle_duda_funciones import conectar_db, obtener_detalle_duda, votar_positivo_comentario, votar_negativo_comentario, borrar_comentario, agregar_comentario
from funciones.publicar_duda_funciones import guardar_nueva_duda,obtener_ultima_duda
from funciones.auth_funciones import usuario_ya_autenticado,iniciar_sesion
from ia.clasificador_texto import TextClassifier



class ExplorarResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('consulta', type=str, required=True)
        parser.add_argument('carrera', type=str)
        parser.add_argument('curso', type=str)
        parser.add_argument('imagen', type=str)
        parser.add_argument('page', type=int, default=1)  # Agregamos los argumentos de paginación
        parser.add_argument('per_page', type=int, default=9)
        args = parser.parse_args()

        consulta = args['consulta']
        carrera = args['carrera']
        curso = args['curso']
        imagen = args['imagen']
        page = args['page']  # Obtenemos el valor de 'page' del argumento
        per_page = args['per_page']

        # Llamamos a la función para obtener las dudas filtradas
        dudas_filtradas = obtener_dudas(consulta, carrera, curso, imagen,page,per_page)
        
        # Devolvemos las dudas filtradas en formato JSON
        return jsonify({'dudas': dudas_filtradas})
   
    def get(self):
        parametros_dudas = obtener_parametros_dudas()
        return jsonify({'dudas': parametros_dudas})


class PerfilResource(Resource):
    def post(self, correo_usuario):
        total_votos_positivos, total_votos_negativos = obtener_total_votos(correo_usuario)

        parser = reqparse.RequestParser()
        parser.add_argument('consulta', type=str, required=True)
        parser.add_argument('carrera', type=str)
        parser.add_argument('curso', type=str)
        args = parser.parse_args()

        consulta = args['consulta']
        carrera = args['carrera']
        curso = args['curso']
        print(curso)
    

        dudas_filtradas = obtener_dudas_usuario(correo_usuario,consulta, carrera, curso)
        
        return {
            'dudas': dudas_filtradas,
            'total_votos_positivos': total_votos_positivos,
            'total_votos_negativos': total_votos_negativos
        }
    
    def get(self, correo_usuario):
        dudas_usuario = obtener_dudas_usuario(correo_usuario)
        total_votos_positivos, total_votos_negativos = obtener_total_votos(correo_usuario)
        dudas_en_json = [{
            '_id': str(duda['_id']),
            'correo':duda.get('correo_usuario',''),
            'titulo': duda.get('titulo', ''),
            'descripcion': duda.get('texto', ''),
            'imagen': duda.get('imagen', '')
        } for duda in dudas_usuario]
        return {
            'dudas': dudas_en_json,
            'total_votos_positivos': total_votos_positivos,
            'total_votos_negativos': total_votos_negativos
        }

    def delete(self, correo_usuario):
        parser = reqparse.RequestParser()
        parser.add_argument('duda_id', type=str, required=True)  # Espera el ID de la duda en el cuerpo JSON
        args = parser.parse_args()
        duda_id = args['duda_id']

        if borrar_duda_por_id(duda_id, correo_usuario):
            # Lógica para obtener las dudas actualizadas después de la eliminación
            dudas_actualizadas = obtener_dudas_usuario(correo_usuario)

            # Convierte las dudas a formato JSON y devuelve un mensaje de éxito
            dudas_en_json = [
                {
                    '_id': str(duda['_id']),
                    'titulo': duda.get('titulo', ''),
                    'descripcion': duda.get('texto', ''),
                    'imagen': duda.get('imagen', '')
                } for duda in dudas_actualizadas
            ]

            return {'message': 'Duda eliminada correctamente', 'dudas': dudas_en_json}, 200
        else:
            # Si hay un problema al borrar la duda, devuelve un mensaje de error
            return {'message': 'Duda no encontrada o no tienes permisos para borrarla'}, 404


class DetalleDudaResource(Resource):


    def get(self, duda_id):
        duda = obtener_detalle_duda(duda_id)
        if duda:
            
            duda_en_json = {
                '_id': str(duda['_id']),
                'titulo': duda.get('titulo', ''),
                'curso': duda.get('curso', ''),
                'correo': duda.get('correo', ''),
                'asignatura': duda.get('asignatura', ''),
                'imagen': duda.get('imagen', ''),
                'carrera': duda.get('carrera', ''),
                'dificultad': duda.get('dificultad', ''),
                'descripcion': duda.get('texto', ''),
                'comentarios': duda.get('comentario', []),
            }
            return jsonify({'duda': duda_en_json})
        else:
            return jsonify({'message': 'Duda no encontrada'}), 404
        
    def post(self, duda_id):
        data = request.get_json()
        data['fecha_agregado'] = datetime.now()
        resultado = agregar_comentario(duda_id, data)

        if resultado:
            return {'message': 'Comentario agregado correctamente'}, 201
        else:
            return {'message': 'Error al agregar el comentario'}, 500

    
    def delete(self,duda_id):
        data = request.form
        comentario_index = int(request.form.get('comentario_index'))

        print(comentario_index)
        resultado = borrar_comentario(duda_id, comentario_index)

        if resultado:
            return {'message': 'Comentario borrado correctamente'}, 200
        else:
            return {'message': 'Error al borrar el comentario'}, 500



class PublicarDudaResource(Resource):
    def get(self):
        duda = obtener_ultima_duda()
        if duda:
            duda_en_json = {
                '_id': str(duda['_id']),
                'titulo': duda.get('titulo', ''),
                'descripcion': duda.get('descripcion', ''),
                'imagen': duda.get('imagen', '')[:10],  
                'carrera': duda.get('carrera', ''),  
                'curso': duda.get('curso', ''),  
                'asignatura': duda.get('asignatura', ''),  
                'dificultad': duda.get('dificultad', ''), 
                'correo_usuario': duda.get('correo_usuario', ''),  
                'comentario': duda.get('comentario', [])  
            }
            return jsonify({'duda': duda_en_json})
        else:
            return jsonify({'message': 'Duda no encontrada'}), 404
        
    


class SesionResource(Resource):
    def get(self):
        if usuario_ya_autenticado():
            correo = session.get('correo_usuario')
            nombre = session.get('nombre_usuario')
            nia = session.get('nia_usuario')  # Agregar la obtención del NIA
            contraseña = session.get('contraseña_usuario')  # Agregar la obtención de la contraseña

            if correo and nombre:
                user_json = {
                    'correo': correo,
                    'nombre': nombre,
                    'nia': nia,  
                    'contrasena': contraseña,  
                }
            
                response_json = json.dumps(user_json)
            
                return response_json, 200, {'Content-Type': 'application/json'}
            else:
                return json.dumps({'message': 'No se encontraron datos de usuario en la sesión'}), 401, {'Content-Type': 'application/json'}
        else:
            return json.dumps({'message': 'Acceso no autorizado'}), 401, {'Content-Type': 'application/json'}

class ComentariosResource(Resource):
    def get(self):
        
        correo_usuario = session.get('correo_usuario')
        _, notificaciones_collection = conectar_db()
        comentarios = list(notificaciones_collection.find({'correo_usuario_duda': correo_usuario}))

       
        comentarios_formateados = []
        for comentario in comentarios:
            comentario_formateado = {
                '_id':str(comentario['_id']),
                'duda_id': str(comentario['duda_id']),
                'nombre_usuario_comentario': comentario['nombre_usuario_comentario'],
                'asignatura': comentario['asignatura']
            }
            comentarios_formateados.append(comentario_formateado)

        
        comentarios_json = json.dumps(comentarios_formateados, ensure_ascii=False)

       
        return jsonify(json.loads(comentarios_json))



class NotificacionesResource(Resource):
    def delete(self, notificacion_id):
        
        correo_usuario = session.get('correo_usuario')
        _, notificaciones_collection = conectar_db()
        notificacion_id_obj = ObjectId(notificacion_id)
        
        resultado = notificaciones_collection.delete_one({'_id': notificacion_id_obj, 'correo_usuario_duda': correo_usuario})

        if resultado.deleted_count == 1:
            return {'mensaje': 'Notificación eliminada correctamente'}, 200
        else:
            return {'mensaje': 'No se encontró la notificación o no tienes permisos para eliminarla'}, 404


class PrediccionResource(Resource):
    def post(self):
        try:
            imagen_bytes = request.data
            imagen_io = io.BytesIO(imagen_bytes)

            imagen_pil = Image.open(imagen_io)

            modelo_path = 'text_classifier_model.joblib'  # Ajusta la ruta según la ubicación de tu modelo
            model = joblib.load(modelo_path)

            texto_extraido = pytesseract.image_to_string(imagen_pil)
            

            clase_predicha = model.predict([texto_extraido])
            print(clase_predicha)

            # Devuelve un diccionario serializable a JSON con la asignatura predicha
            return {'asignatura': clase_predicha[0]}, 200

        except Exception as e:
            print(f"Error al procesar la imagen: {e}")
            # Devuelve un diccionario con el error y un código de estado 500
            return {'error': 'Error en la predicción'}, 500

        