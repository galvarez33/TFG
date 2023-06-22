from flask import Flask, render_template

app = Flask(__name__)
app.static_folder = 'static'


@app.route('/home')
def index():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

if __name__ == '__main__':
    app.run(port=5004)
