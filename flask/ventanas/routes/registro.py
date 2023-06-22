from flask import Flask, render_template, request, redirect, url_for,re

app = Flask(__name__)

class RegistroUsuario:
    def __init__(self):
        self.usuarios = []
        

    def agregar_usuario(self, usuario):
        self.usuarios.append(usuario)

    def buscar_usuario(self, correo):
        for usuario in self.usuarios:
            if usuario['correo'] == correo:
                return usuario
        return None

registro = RegistroUsuario()

@app.route('/')
def index():
    return render_template('registro.html')

@app.route('/registro', methods=['POST'])
def registro():
    correo = request.form['correo']
    nombre_usuario = request.form['nombre_usuario']
    contraseña = request.form['contraseña']

    # Validar el formato del correo
    correo_valido = re.match(r'^[a-zA-Z0-9]+@usp\.ceu\.es$', correo)
    if not correo_valido:
        return render_template('registro.html', error='El correo electrónico no tiene el formato válido.')

    # Validar la longitud del NIA
    nia = request.form['nia']
    if len(nia) != 6 or not nia.isdigit():
        return render_template('registro.html', error='El NIA debe ser un número de 6 dígitos.')

    usuario_existente = registro.buscar_usuario(correo)
    if usuario_existente:
        return render_template('registro.html', error='El correo electrónico ya está registrado.')

    nuevo_usuario = {
        'correo': correo,
        'nombre_usuario': nombre_usuario,
        'contraseña': contraseña
    }

    registro.agregar_usuario(nuevo_usuario)
    print(usuarios)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
