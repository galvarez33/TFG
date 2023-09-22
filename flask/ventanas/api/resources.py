from flask_restful import Resource,reqparse
from flask import jsonify
from flask_jwt import jwt_required
from funciones.explorar_funciones import obtener_parametros_dudas
from funciones.perfil_funciones import obtener_dudas_usuario,borrar_duda_por_id
from funciones.detalle_duda_funciones import conectar_db, obtener_detalle_duda, votar_positivo_comentario, votar_negativo_comentario, borrar_comentario, agregar_comentario
from funciones.publicar_duda_funciones import guardar_nueva_duda,obtener_ultima_duda

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
        # Aquí obtienes los detalles de la duda con el ID especificado desde tu base de datos
        duda = obtener_ultima_duda()
        if duda:
            # Si la duda existe, la devuelves como un JSON
            duda_en_json = {
                '_id': str(duda['_id']),
                'titulo': duda.get('titulo', ''),
                'descripcion': duda.get('descripcion', ''),
                'imagen': duda.get('imagen', ''),  # Agrega el campo imagen si está disponible
                'carrera': duda.get('carrera', ''),  # Agrega el campo carrera si está disponible
                'curso': duda.get('curso', ''),  # Agrega el campo curso si está disponible
                'asignatura': duda.get('asignatura', ''),  # Agrega el campo asignatura si está disponible
                'dificultad': duda.get('dificultad', ''),  # Agrega el campo dificultad si está disponible
                'correo_usuario': duda.get('correo_usuario', ''),  # Agrega el campo correo_usuario si está disponible
                'comentario': duda.get('comentario', [])  # Agrega el campo comentario si está disponible
            }
            return jsonify({'duda': duda_en_json})
        else:
            # Si la duda no existe, devuelves un mensaje de error y un código de estado 404 (No encontrado)
            return jsonify({'message': 'Duda no encontrada'}), 404
        
    

