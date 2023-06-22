from flask import Flask, render_template, request, redirect, session, url_for
from pymongo import MongoClient
import re
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'practicaceu@gmail.com'
app.config['MAIL_PASSWORD'] = 'pzrwkjjftegjcwwy'
app.secret_key = '12345'

mail = Mail(app)
client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
db = client['TFG']
collection = db['usuarios']


@app.route('/home')
def index():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['correo']
        password = request.form['contrasena']

        user = collection.find_one({'correo': username, 'contraseña': password})
        if user:
            session['logged_user'] = user['correo']
            return redirect(url_for('restricted'))
        else:
            error = 'El Correo o Contraseña son incorrectos'
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        nia = request.form['nia']

        correo_valido = re.match(r'^[a-zA-Z0-9.]+@usp\.ceu\.es$', correo)
        if not correo_valido:
            error = 'El correo electrónico no tiene el formato válido.'
            return render_template('registro.html', error=error)

        if len(nia) != 6 or not nia.isdigit():
            error = 'El NIA debe ser un número de 6 dígitos.'
            return render_template('registro.html', error=error)

        usuario_existente = collection.count_documents({'correo': correo})
        if usuario_existente > 0:
            error = "El correo electrónico ya está registrado."
            return render_template('registro.html', error=error)

        if not re.search(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{5,}$', contraseña):
            error = 'La contraseña debe tener al menos 5 caracteres, una mayúscula, una minúscula y un número.'
            return render_template('registro.html', error=error)

        datos_usuario = {
            'correo': correo,
            'contraseña': contraseña,
            'nia': nia,
            
        }

        enviar_correo_verificacion(correo, contraseña, nia)
        return redirect(url_for('login'))

    return render_template('registro.html')


def enviar_correo_verificacion(correo, contraseña, nia):
    serializer = URLSafeTimedSerializer(app.secret_key)
    token = serializer.dumps(correo, salt='email-confirm')
    url_verificacion = url_for('confirmar_correo', token=token, contraseña=contraseña, nia=nia, _external=True)

    mensaje = Message('Verificación de correo electrónico', sender='ceupractica@gmail.com', recipients=[correo])
    mensaje.body = f'Haz clic en el siguiente enlace para verificar tu correo electrónico: {url_verificacion}'

    mail.send(mensaje)


@app.route('/confirmar-correo/<token>')
def confirmar_correo(token):
    serializer = URLSafeTimedSerializer(app.secret_key)
    try:
        correo = serializer.loads(token, salt='email-confirm', max_age=3600)
        contraseña = request.args.get('contraseña')
        nia = request.args.get('nia')

        datos_usuario = {
            'correo': correo,
            'contraseña': contraseña,
            'nia': nia
        }

        collection.insert_one(datos_usuario)
        return render_template('login.html', correo=correo)
    except:
        return render_template('login.html', error='Token inválido o expirado')


@app.route('/restricted')
def restricted():
    if 'logged_user' in session:
        return render_template('restricted.html')
        
    else:
        return 'Acceso no autorizado'

if __name__ == '__main__':
    app.run(port=5004)
