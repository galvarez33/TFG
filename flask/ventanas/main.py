from flask import Flask, render_template, request, redirect, session, url_for
from pymongo import MongoClient
import re
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True  # Si se utiliza TLS
app.config['MAIL_USERNAME'] = 'practicaceu@gmail.com'
app.config['MAIL_PASSWORD'] = 'pzrwkjjftegjcwwy'
app.secret_key = '1234'  # Reemplaza con tu propia clave secreta

mail = Mail(app)
client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
db = client['TFG']
collection = db['usuarios']


users = []  # Lista para almacenar usuarios registrados

@app.route('/home')
def index():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])

def login():
    if request.method == 'POST':
        username = request.form['correo']
        password = request.form['contrasena']

        # Buscar el usuario en la base de datos
        user_count = collection.count_documents({'correo': f'{username}', 'contraseña': f'{password}'},)
        if user_count > 0:
           # Almacenar estado de inicio de sesión en la sesión
            return redirect(url_for('restricted'))
        else:
            return redirect(url_for('login'))

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

    # Validar la longitud del NIA
        
        if len(nia) != 6 or not nia.isdigit():
            error= 'El NIA debe ser un número de 6 dígitos.'
            return render_template('registro.html', error=error)

        usuario_existente = collection.count_documents({'correo': f'{correo}'})
        if usuario_existente >0:
            error= "El correo electrónico ya está registrado."
            return render_template('registro.html', error=error)

        # Validar la contraseña
        if not re.search(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{5,}$', contraseña):
            error = 'La contraseña debe tener al menos 5 caracteres, una mayúscula, una minúscula y un número.'
            return render_template('registro.html', error=error)



        # Crear el documento del usuario
        datos_usuario = {
            'correo': correo,
            'contraseña': contraseña,
            'nia': nia
        }

        # Insertar el documento en la colección de MongoDB Atlas
        collection.insert_one(datos_usuario)
        enviar_correo_verificacion(correo)
        # Redirigir al usuario a la página de inicio de sesión después del registro exitoso
        return redirect(url_for('login'))

    return render_template('registro.html')


def enviar_correo_verificacion(correo):
    # Generar un token único para el usuario
    serializer = URLSafeTimedSerializer(app.secret_key)
    token = serializer.dumps(correo, salt='email-confirm')

    # Construir el enlace de verificación
    url_verificacion = url_for('confirmar_correo', token=token, _external=True)

    # Crear el mensaje de correo
    mensaje = Message('Verificación de correo electrónico', sender='ceupractica@gmail.com', recipients=[correo])
    mensaje.body = f'Haz clic en el siguiente enlace para verificar tu correo electrónico: {url_verificacion}'

    # Enviar el correo
    mail.send(mensaje)


@app.route('/confirmar-correo/<token>')
def confirmar_correo(token):
    serializer = URLSafeTimedSerializer(app.secret_key)
    try:
        correo = serializer.loads(token, salt='email-confirm', max_age=3600)  # Verificar el token
        # Realizar la acción correspondiente, por ejemplo, activar la cuenta del usuario en la base de datos
        # Puedes mostrar un mensaje de confirmación en esta página
        return render_template('login.html', correo=correo)
    except:
        # Si el token es inválido o ha expirado, puedes mostrar un mensaje de error
        return render_template('login.html', error='Token inválido o expirado')





@app.route('/restricted')
def restricted():
    if 'logged_user' in session:
        return render_template('restricted.html', logged_user=session['logged_user'])
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=5004)
