from flask_restful import Resource,reqparse
from flask import jsonify,session, Response, request
import json

from funciones.explorar_funciones import obtener_parametros_dudas
from funciones.perfil_funciones import obtener_dudas_usuario,borrar_duda_por_id
from funciones.detalle_duda_funciones import conectar_db, obtener_detalle_duda, votar_positivo_comentario, votar_negativo_comentario, borrar_comentario, agregar_comentario
from funciones.publicar_duda_funciones import guardar_nueva_duda,obtener_ultima_duda
from funciones.auth_funciones import usuario_ya_autenticado,iniciar_sesion

class ExplorarResource(Resource):
    def get(self):
        parametros_dudas = obtener_parametros_dudas()
        return {'dudas': parametros_dudas}


class PerfilResource(Resource):
    def get(self, correo_usuario):
        dudas_usuario = obtener_dudas_usuario(correo_usuario)
        dudas_en_json = [{'_id': str(duda['_id']), 'titulo': duda.get('titulo', '')} for duda in dudas_usuario]
        return {'dudas': dudas_en_json}


class DetalleDudaResource(Resource):
    def get(self, duda_id):
        duda = obtener_detalle_duda(duda_id)
        if duda:
            
            duda_en_json = {
                '_id': str(duda['_id']),
                'titulo': duda.get('titulo', ''),
                'descripcion': duda.get('descripcion', ''),
                'comentarios': duda.get('comentario', []),
            }
            return jsonify({'duda': duda_en_json})
        else:
            return jsonify({'message': 'Duda no encontrada'}), 404
        



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
        # Obtén el correo del usuario que ha iniciado sesión
        correo_usuario = session.get('correo_usuario')

        # Establecer la conexión a la base de datos MongoDB
        _, notificaciones_collection = conectar_db()

        # Obtener los comentarios de la colección de notificaciones
        comentarios = list(notificaciones_collection.find({'correo_usuario_duda': correo_usuario}))

        # Formatear comentarios como una lista de diccionarios
        comentarios_formateados = []
        for comentario in comentarios:
            comentario_formateado = {
                'duda_id': str(comentario['duda_id']),
                'nombre_usuario_comentario': comentario['nombre_usuario_comentario'],
                'asignatura': comentario['asignatura']
            }
            comentarios_formateados.append(comentario_formateado)

        # Usar json.dumps con ensure_ascii=False para manejar caracteres especiales correctamente
        comentarios_json = json.dumps(comentarios_formateados, ensure_ascii=False)

        # Usar jsonify para crear la respuesta JSON
        return jsonify(json.loads(comentarios_json))