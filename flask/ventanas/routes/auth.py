from flask import render_template, session, request, redirect, url_for, Blueprint
from pymongo import MongoClient
from bson import ObjectId
import re
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import base64
from datetime import datetime
from . import auth_bp


secret_key ='12345'

client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
db = client['TFG']
collection = db['usuarios']
mail = Mail()

# Ruta para iniciar sesión
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_user' in session:
        return redirect(url_for('auth.restricted'))

    if request.method == 'POST':
        username = request.form['correo']
        password = request.form['contrasena']

        user = collection.find_one({'correo': username, 'contraseña': password})
        if user:
            # Guardar el correo del usuario en la sesión
            session['logged_user'] = {
                'correo': user['correo'],
                'nombre': user['nombre']
            }

            # Guardar el nombre del usuario en la sesión
            session['nombre_usuario'] = user['nombre']

            return redirect(url_for('auth.restricted'))
        else:
            error = 'El correo o la contraseña son incorrectos'
            return render_template('login.html', error=error)

    mensaje_confirmacion = session.pop('mensaje_confirmacion', None)
    return render_template('login.html', mensaje_confirmacion=mensaje_confirmacion)


# Ruta para el registro de usuarios
@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if 'logged_user' in session:
        return redirect(url_for('auth.restricted'))

    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        nia = request.form['nia']
        nombre = request.form['nombre']

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
            'nombre':nombre
        }

        enviar_correo_verificacion(correo, contraseña, nia, nombre )
        session['mensaje_confirmacion'] = 'Se ha enviado un correo de confirmación a tu dirección de correo electrónico.'

        return redirect(url_for('auth.login'))

    return render_template('registro.html')


def generar_token(correo):
    serializer = URLSafeTimedSerializer(secret_key)
    token = serializer.dumps({'correo': correo}, salt='restablecer-contrasena')
    return token


def obtener_correo_desde_token(token):
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        data = serializer.loads(token, salt='restablecer-contrasena', max_age=3600)
        correo = data['correo']
        return correo
    except:
        return None


def enviar_correo_verificacion(correo, contraseña, nia, nombre ):
    token = generar_token(correo)
    url_verificacion = url_for('auth.confirmar_correo', token=token, contraseña=contraseña, nia=nia,nombre=nombre, _external=True)

    mensaje = Message('Verificación de correo electrónico', sender='ceupractica@gmail.com', recipients=[correo])
    mensaje.body = f'Haz clic en el siguiente enlace para verificar tu correo electrónico: {url_verificacion}'

    mail.send(mensaje)


@auth_bp.route('/confirmar-correo/<token>')
def confirmar_correo(token):
    correo = obtener_correo_desde_token(token)
    if correo:
        contraseña = request.args.get('contraseña')
        nia = request.args.get('nia')
        nombre = request.args.get('nombre')

        datos_usuario = {
            'correo': correo,
            'contraseña': contraseña,
            'nia': nia,
            'nombre': nombre
        }

        collection.insert_one(datos_usuario)
        return render_template('login.html', correo=correo)
    else:
        return render_template('login.html', error='Token inválido o expirado')


@auth_bp.route('/restricted')
def restricted():
    logged_user = session.get('logged_user')

    if 'logged_user' in session:
        return render_template('restricted.html', logged_user=logged_user, restricted_endpoint=url_for('auth.restricted'))
    else:
        return 'Acceso no autorizado'


@auth_bp.route('/cierre', methods=['GET', 'POST'])
def cierre():
    logged_user = session.get('logged_user')
    if request.method == 'POST':
        confirm = request.form.get('confirm')
        if confirm == 'yes':
            session.clear()
            return redirect(url_for('home.home'))
        elif confirm == 'no':
            return redirect(url_for('auth.restricted'))
    return render_template('cierre.html', logged_user=logged_user)


@auth_bp.route('/contrasena_olvidada', methods=['GET', 'POST'])
def contrasena_olvidada():
    if 'logged_user' in session:
        return redirect(url_for('auth.restricted'))

    if request.method == 'POST':
        correo = request.form['correo']
        resultado = collection.find_one({'correo': correo})
        if resultado:
            enviar_correo_restablecer_contrasena(correo)
            session['mensaje_confirmacion'] = 'Se ha enviado un correo de restablecimiento de contraseña a tu dirección de correo electrónico.'
            return redirect(url_for('auth.login'))
        else:
            error = 'El correo introducido no existe'
            return render_template('contrasena_olvidada.html', error=error)


    return render_template('contrasena_olvidada.html')


def enviar_correo_restablecer_contrasena(correo):
    token = generar_token(correo)  # Generar el token con el correo electrónico
    url_restablecer = url_for('auth.restablecer_contrasena', correo=correo, token=token, _external=True)

    mensaje = Message('Restablecer contraseña', sender='practicaceu@gmail.com', recipients=[correo])
    mensaje.body = f'Haz clic en el siguiente enlace para restablecer tu contraseña: {url_restablecer}'

    mail.send(mensaje)


@auth_bp.route('/restablecer_contrasena/<correo>/<token>', methods=['GET', 'POST'])
def restablecer_contrasena(correo, token):
    print(correo)
    if request.method == 'POST':
        nueva_contrasena = request.form['nueva_contrasena']
        confirmar_contrasena = request.form['confirmar_contrasena']
        token = request.form['token']  # Agrega esta línea para obtener el token del formulario

        # Validar que las contraseñas coinciden
        if nueva_contrasena != confirmar_contrasena:
            return render_template('restablecer_contrasena.html', error='Las contraseñas no coinciden', correo=correo, token=token)
        
        if not re.search(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{5,}$', nueva_contrasena):
            error = 'La contraseña debe tener al menos 5 caracteres, una mayúscula, una minúscula y un número.'
            return render_template('restablecer_contrasena.html', error=error, correo=correo, token=token)
            
        # Actualizar la contraseña en la base de datos
        result = collection.update_one({'correo': correo}, {'$set': {'contraseña': nueva_contrasena}})
        print(correo,token, nueva_contrasena)
        print(result.modified_count) 

        # Redirigir a la página de inicio de sesión después de restablecer la contraseña
        session['mensaje_confirmacion'] = 'La contraseña se ha restablecido correctamente. Inicia sesión con tu nueva contraseña.'
        return redirect(url_for('auth.login'))

    return render_template('restablecer_contrasena.html', correo=correo, token=token)	
