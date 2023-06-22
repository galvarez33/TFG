from flask import Flask, render_template, request, redirect, session,url_for
from pymongo import MongoClient


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
        password = request.form['contraseña']

        # Comprobar si el usuario y la contraseña coinciden en la lista de usuarios
        if any(user[0] == username and user[1] == password for user in users):
            session['logged_user'] = username  # Almacenar estado de inicio de sesión en la sesión
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
