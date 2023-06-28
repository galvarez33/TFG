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
app.config['MAIL_PASSWORD'] = 'lkytkgkbhirfyxlv'
app.secret_key = '12345'

mail = Mail(app)
client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
db = client['TFG']
collection = db['usuarios']


@app.route('/home')
def home():
    logged_user = session.get('logged_user')
    return render_template('home.html', logged_user=logged_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_user' in session:
        return redirect(url_for('restricted'))

    if request.method == 'POST':
        username = request.form['correo']
        password = request.form['contrasena']

        user = collection.find_one({'correo': username, 'contraseña': password})
        if user:
            session['logged_user'] = user['correo']
            return redirect(url_for('restricted'))
        else:
            error = 'El correo o la contraseña son incorrectos'
            return render_template('login.html', error=error)

    mensaje_confirmacion = session.pop('mensaje_confirmacion', None)
    return render_template('login.html', mensaje_confirmacion=mensaje_confirmacion)


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if 'logged_user' in session:
        return redirect(url_for('restricted'))

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
        session['mensaje_confirmacion'] = 'Se ha enviado un correo de confirmación a tu dirección de correo electrónico.'

        return redirect(url_for('login'))

    return render_template('registro.html')


def generar_token(correo):
    serializer = URLSafeTimedSerializer(app.secret_key)
    token = serializer.dumps({'correo': correo}, salt='restablecer-contrasena')
    return token


def obtener_correo_desde_token(token):
    serializer = URLSafeTimedSerializer(app.secret_key)
    try:
        data = serializer.loads(token, salt='restablecer-contrasena', max_age=3600)
        correo = data['correo']
        return correo
    except:
        return None


def enviar_correo_verificacion(correo, contraseña, nia):
    token = generar_token(correo)
    url_verificacion = url_for('confirmar_correo', token=token, contraseña=contraseña, nia=nia, _external=True)

    mensaje = Message('Verificación de correo electrónico', sender='ceupractica@gmail.com', recipients=[correo])
    mensaje.body = f'Haz clic en el siguiente enlace para verificar tu correo electrónico: {url_verificacion}'

    mail.send(mensaje)


@app.route('/confirmar-correo/<token>')
def confirmar_correo(token):
    correo = obtener_correo_desde_token(token)
    if correo:
        contraseña = request.args.get('contraseña')
        nia = request.args.get('nia')

        datos_usuario = {
            'correo': correo,
            'contraseña': contraseña,
            'nia': nia
        }

        collection.insert_one(datos_usuario)
        return render_template('login.html', correo=correo)
    else:
        return render_template('login.html', error='Token inválido o expirado')


@app.route('/restricted')
def restricted():
    logged_user = session.get('logged_user')

    if 'logged_user' in session:
        return render_template('restricted.html', logged_user=logged_user)
    else:
        return 'Acceso no autorizado'


@app.route('/cierre', methods=['GET', 'POST'])
def cierre():
    logged_user = session.get('logged_user')
    if request.method == 'POST':
        confirm = request.form.get('confirm')
        if confirm == 'yes':
            session.clear()
            return redirect(url_for('home'))
        elif confirm == 'no':
            return redirect(url_for('restricted'))
    return render_template('cierre.html', logged_user=logged_user)


@app.route('/contrasena_olvidada', methods=['GET', 'POST'])
def contrasena_olvidada():
    if 'logged_user' in session:
        return redirect(url_for('restricted'))

    if request.method == 'POST':
        correo = request.form['correo']
        enviar_correo_restablecer_contrasena(correo)
        session['mensaje_confirmacion'] = 'Se ha enviado un correo de restablecimiento de contraseña a tu dirección de correo electrónico.'
        return redirect(url_for('login'))

    return render_template('contrasena_olvidada.html')


def enviar_correo_restablecer_contrasena(correo):
    token = generar_token(correo)  # Generar el token con el correo electrónico
    url_restablecer = url_for('restablecer_contrasena', correo=correo, token=token, _external=True)

    mensaje = Message('Restablecer contraseña', sender='practicaceu@gmail.com', recipients=[correo])
    mensaje.body = f'Haz clic en el siguiente enlace para restablecer tu contraseña: {url_restablecer}'

    mail.send(mensaje)


@app.route('/restablecer_contrasena/<correo>/<token>', methods=['GET', 'POST'])
def restablecer_contrasena(correo, token):
    print(correo)
    if request.method == 'POST':
        nueva_contrasena = request.form['nueva_contrasena']
        confirmar_contrasena = request.form['confirmar_contrasena']
        print(correo,nueva_contrasena)

        # Validar que las contraseñas coinciden
        if nueva_contrasena != confirmar_contrasena:
            return render_template('restablecer_contrasena.html', error='Las contraseñas no coinciden')

        # Obtener el correo electrónico a partir del token (opcional)
        # correo = obtener_correo_desde_token(token)

        # Actualizar la contraseña en la base de datos
        result = collection.update_one({'correo': correo}, {'$set': {'contraseña': nueva_contrasena}})
        print(result.modified_count) 

        # Redirigir a la página de inicio de sesión después de restablecer la contraseña
        session['mensaje_confirmacion'] = 'La contraseña se ha restablecido correctamente. Inicia sesión con tu nueva contraseña.'
        return redirect(url_for('login'))

    return render_template('restablecer_contrasena.html', correo=correo, token=token)


if __name__ == '__main__':
    app.run(port=5004)
