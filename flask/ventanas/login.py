from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Datos de ejemplo (usuario y contraseña)
usuario_valido = {
    'nombre': 'admin',
    'contraseña': '123456'
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        contraseña = request.form['contraseña']

        if nombre_usuario == usuario_valido['nombre'] and contraseña == usuario_valido['contraseña']:
            return redirect('/index')
        else:
            error = 'Credenciales inválidas. Inténtalo de nuevo.'
            return render_template('login.html', error=error)

    # Manejar la solicitud GET
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000)
