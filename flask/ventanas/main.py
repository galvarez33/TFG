from flask import Flask, session
from flask_mail import Mail, Message
from routes import auth_bp, home_bp, publicar_duda_bp, explorar_bp, perfil_bp, detalle_duda_bp
from api.resources import ExplorarResource, PerfilResource, DetalleDudaResource, PublicarDudaResource
from flask_restful import Api 


app = Flask(__name__)
api =Api(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'practicaceu@gmail.com'
app.config['MAIL_PASSWORD'] = 'lkytkgkbhirfyxlv'

mail = Mail(app)


app.secret_key = '12345'
app.debug = False

api.add_resource(ExplorarResource, '/api/explorar')
api.add_resource(PerfilResource, '/api/perfil/<string:correo_usuario>')
api.add_resource(DetalleDudaResource, '/api/detalle_duda/<duda_id>')
api.add_resource(PublicarDudaResource, '/api/publicar_duda')



app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(publicar_duda_bp)
app.register_blueprint(explorar_bp)
app.register_blueprint(perfil_bp)
app.register_blueprint(detalle_duda_bp, url_prefix='/detalle_duda')



if __name__ == '__main__':
    app.debug = True 
    app.run(port=5001)
