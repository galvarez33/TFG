from flask import Flask
from flask_mail import Mail
from flask_cors import CORS
from flask_restful import Api
from routes import auth_bp, home_bp, publicar_duda_bp, explorar_bp, perfil_bp, detalle_duda_bp
from api.resources import ExplorarResource, PerfilResource, DetalleDudaResource, PublicarDudaResource, SesionResource, ComentariosResource, NotificacionesResource,PrediccionResource,RankingResource

app = Flask(__name__)
api = Api(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'practicaceu@gmail.com'
app.config['MAIL_PASSWORD'] = 'lkytkgkbhirfyxlv'

mail = Mail(app)

app.secret_key = '12345'
ranking_dict = {}
ranking_resource_instance = RankingResource("ranking.json")


# Agrega tus recursos de API a la ruta correspondiente
api.add_resource(ExplorarResource, '/api/explorar')
api.add_resource(PerfilResource, '/api/perfil/<string:correo_usuario>')
api.add_resource(DetalleDudaResource, '/api/detalle_duda/<string:duda_id>')
api.add_resource(PublicarDudaResource, '/api/publicar_duda')
api.add_resource(SesionResource, '/api/sesion')
api.add_resource(ComentariosResource, '/api/comentarios')
api.add_resource(NotificacionesResource, '/api/notificaciones/<string:notificacion_id>')
api.add_resource(PrediccionResource, '/api/predecir_texto')
api.add_resource(RankingResource, '/api/ranking/<string:correo_usuario>', resource_class_kwargs={'ranking_file_path': ranking_resource_instance.ranking_file_path})



# Registra tus blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(publicar_duda_bp)
app.register_blueprint(explorar_bp)
app.register_blueprint(perfil_bp)
app.register_blueprint(detalle_duda_bp)


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.debug = True 
    app.run(port=5001)
    CORS(app) 
