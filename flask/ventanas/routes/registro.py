from flask import Flask, render_template, request, redirect, url_for

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

    usuario_existente = registro.buscar_usuario(correo)
    if usuario_existente:
        return render_template('registro.html', error='El correo electrónico ya está registrado.')

    nuevo_usuario = {
        'correo': correo,
        'nombre_usuario': nombre_usuario,
        'contraseña': contraseña
    }

    registro.agregar_usuario(nuevo_usuario)

    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
