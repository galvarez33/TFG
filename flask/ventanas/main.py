from flask import Flask, render_template, request, redirect, session, url_for
from pymongo import MongoClient
from bson import ObjectId
import re
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import base64
from math import ceil
from flask_paginate import Pagination, get_page_parameter, get_page_args



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
form_collection= db['publicar_duda'] 




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
            # Guardar el correo del usuario en la sesión
            session['logged_user'] = {
                'correo': user['correo'],
                'nombre': user['nombre']
            }


            # Guardar el nombre del usuario en la sesión
            session['nombre_usuario'] = user['nombre']

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


def enviar_correo_verificacion(correo, contraseña, nia, nombre ):
    token = generar_token(correo)
    url_verificacion = url_for('confirmar_correo', token=token, contraseña=contraseña, nia=nia,nombre=nombre, _external=True)

    mensaje = Message('Verificación de correo electrónico', sender='ceupractica@gmail.com', recipients=[correo])
    mensaje.body = f'Haz clic en el siguiente enlace para verificar tu correo electrónico: {url_verificacion}'

    mail.send(mensaje)


@app.route('/confirmar-correo/<token>')
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
        resultado = collection.find_one({'correo': correo})
        if resultado:
            enviar_correo_restablecer_contrasena(correo)
            session['mensaje_confirmacion'] = 'Se ha enviado un correo de restablecimiento de contraseña a tu dirección de correo electrónico.'
            return redirect(url_for('login'))
        else:
            error = 'El correo introducido no existe'
            return render_template('contrasena_olvidada.html', error=error)


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
        return redirect(url_for('login'))

    return render_template('restablecer_contrasena.html', correo=correo, token=token)



@app.route('/publicar_duda', methods=['GET', 'POST'])
def publicar_duda():
    logged_user = session.get('logged_user')
    if request.method == 'POST':
        imagen = request.files['imagen']
        titulo = request.form['titulo']
        texto = request.form['texto']
        carrera = request.form['carrera']
        curso = request.form['curso']
        asignatura = request.form['asignatura']
        dificultad = int(request.form['dificultad'])  # Convertir a entero

        if imagen:
            imagen_base64 = base64.b64encode(imagen.read()).decode('utf-8')

        # Guardar la información en la base de datos
        form_data = {
            'imagen': imagen_base64,
            'titulo': titulo,
            'texto': texto,
            'carrera': carrera,
            'curso': curso,
            'asignatura': asignatura,
            'dificultad': dificultad,  # Agregar la dificultad al documento
            'comentario':[]
        }
        form_collection.insert_one(form_data)

        return redirect(url_for('explorar'))

    return render_template('publicar_duda.html', logged_user=logged_user)

@app.route('/explorar', methods=['GET', 'POST'])
def explorar():
    if request.method == 'POST':
        # Verificar si el usuario está autenticado antes de procesar la solicitud POST
        logged_user = session.get('logged_user')
        if not logged_user:
            return 'Acceso no autorizado'

        consulta = request.form.get('consulta', '')
        carrera = request.form.get('carrera', '')
        curso = request.form.get('curso', '')

        # Aplicar filtros si se han seleccionado valores
        filtros = {}
        if carrera:
            filtros['carrera'] = carrera
        if curso:
            filtros['curso'] = curso

        # Consultar las dudas con los filtros aplicados
        dudas = form_collection.find({'titulo': {'$regex': consulta, '$options': 'i'}, **filtros})
    else:
        # Si la solicitud no es POST, mostrar todas las dudas sin filtros
        dudas = form_collection.find()

    # Obtener el número de página actual y la cantidad de elementos por página
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    per_page = 9  # Mostrar 9 elementos por página

    # Calcular el desplazamiento para la consulta en la base de datos
    offset = (page - 1) * per_page

    # Consultar las dudas con el límite y desplazamiento adecuados
    dudas = dudas.skip(offset).limit(per_page)

    # Obtener el total de dudas para la paginación
    total_dudas = form_collection.count_documents({})

    # Crear el objeto de paginación
    pagination = Pagination(page=page, per_page=per_page, total=total_dudas, css_framework='bootstrap4')

    return render_template('explorar.html', dudas=dudas, pagination=pagination)



def obtener_detalle_duda(duda_id):
    # Convertir el duda_id a ObjectId
    object_id = ObjectId(duda_id)
    duda = form_collection.find_one({'_id': object_id})

    return duda




@app.route('/detalle_duda/<duda_id>', methods=['GET', 'POST'])
def detalle_duda(duda_id):
    # Verificar si el usuario está autenticado
    logged_user = session.get('logged_user')
    if not logged_user:
        return 'Acceso no autorizado'

    # Obtener el nombre del usuario desde la sesión
    nombre_usuario = session.get('nombre_usuario')

    duda = obtener_detalle_duda(duda_id)
    
    if duda:
        if request.method == 'POST':
            # Obtener el comentario del formulario enviado
            nuevo_comentario = request.form.get('comentario')
            imagen = request.files['imagen']

            # Convertir la imagen en Base64
            if imagen:
                imagen_base64 = base64.b64encode(imagen.read()).decode('utf-8')
            else:
                imagen_base64 = None

            # Crear la tupla de comentario e imagen
            comentario_con_imagen = (nombre_usuario, nuevo_comentario, imagen_base64)

            # Actualizar la colección con el nuevo comentario agregado a la lista
            form_collection.update_one(
                {'_id': duda['_id']},
                {'$push': {'comentario': comentario_con_imagen}}
            )

            # Redirigir a la página de detalle de la duda para mostrar el cambio
            return redirect(url_for('detalle_duda', duda_id=duda['_id']))

        # Verificar si se ha enviado una solicitud para borrar un comentario
        comentario_index = request.args.get('comentario_index')
        if comentario_index is not None:
            # Convertir el índice del comentario a entero
            comentario_index = int(comentario_index)
            # Eliminar el comentario con el índice proporcionado
            form_collection.update_one(
                {'_id': duda['_id']},
                {'$unset': {f'comentario.{comentario_index}': 1}}
            )
            # Eliminar el elemento vacío del arreglo
            form_collection.update_one(
                {'_id': duda['_id']},
                {'$pull': {'comentario': None}}
            )
            # Redirigir a la página de detalle de la duda para mostrar el cambio
            return redirect(url_for('detalle_duda', duda_id=duda['_id']))

        return render_template('detalle_duda.html', duda=duda, logged_user=logged_user, nombre_usuario=nombre_usuario)
    else:
        # Si no se encuentra la duda con el ID proporcionado, muestra un mensaje de error
        return render_template('error.html', mensaje='Duda no encontrada')





@app.route('/borrar_comentario/<duda_id>/<int:comentario_index>', methods=['POST'])
def borrar_comentario(duda_id, comentario_index):
    # Verificar si el usuario está autenticado
    logged_user = session.get('logged_user')
    if not logged_user:
        return 'Acceso no autorizado'

    # Obtener el nombre del usuario desde la sesión
    nombre_usuario = session.get('nombre_usuario')

    # Buscar la duda por su ID en la base de datos
    duda = form_collection.find_one({'_id': ObjectId(duda_id)})

    if duda:
        # Obtener la lista de comentarios
        comentarios = duda.get('comentario', [])

        # Verificar si el índice del comentario está dentro de los límites válidos
        if 0 <= comentario_index < len(comentarios):
            # Verificar si el usuario autenticado es el que publicó el comentario
            if nombre_usuario == comentarios[comentario_index][0]:
                # Eliminar el comentario del índice proporcionado
                comentarios.pop(comentario_index)

                # Actualizar el documento en la base de datos con la nueva lista de comentarios
                form_collection.update_one(
                    {'_id': duda['_id']},
                    {'$set': {'comentario': comentarios}}
                )

        # Redirigir a la página de detalle de la duda para mostrar el cambio
        return redirect(url_for('detalle_duda', duda_id=duda_id))
    else:
        return 'Acceso no autorizado'









if __name__ == '__main__':
    app.run(port=5001)