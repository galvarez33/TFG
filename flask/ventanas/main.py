from flask import Flask
from flask_mail import Mail
from flask_cors import CORS
from flask_restful import Api
from routes import auth_bp, home_bp, publicar_duda_bp, explorar_bp, perfil_bp, detalle_duda_bp
from api.resources import ExplorarResource, PerfilResource, DetalleDudaResource, PublicarDudaResource, SesionResource, ComentariosResource, NotificacionesResource,PrediccionResource

app = Flask(__name__)
api = Api(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'practicaceu@gmail.com'
app.config['MAIL_PASSWORD'] = 'lkytkgkbhirfyxlv'

mail = Mail(app)

app.secret_key = '12345'

# Agrega tus recursos de API a la ruta correspondiente
api.add_resource(ExplorarResource, '/api/explorar')
api.add_resource(PerfilResource, '/api/perfil/<string:correo_usuario>')
api.add_resource(DetalleDudaResource, '/api/detalle_duda/<string:duda_id>')
api.add_resource(PublicarDudaResource, '/api/publicar_duda')
api.add_resource(SesionResource, '/api/sesion')
api.add_resource(ComentariosResource, '/api/comentarios')
api.add_resource(NotificacionesResource, '/api/notificaciones/<string:notificacion_id>')
api.add_resource(PrediccionResource, '/api/predecir_texto')



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
