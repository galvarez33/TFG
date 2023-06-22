from flask import Flask, render_template, request, redirect, session, url_for
from pymongo import MongoClient
import re


app = Flask(__name__)
app.secret_key = '1234'  # Reemplaza con tu propia clave secreta
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

        correo_valido = re.match(r'^[a-zA-Z0-9]+@usp\.ceu\.es$', correo)
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

        # Redirigir al usuario a la página de inicio de sesión después del registro exitoso
        return redirect(url_for('login'))

    return render_template('registro.html')

@app.route('/restricted')
def restricted():
    if 'logged_user' in session:
        return render_template('restricted.html', logged_user=session['logged_user'])
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=5004)
