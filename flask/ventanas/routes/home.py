from flask import Flask, render_template

app = Flask(__name__)

@app.route('/home')
def home():
    title = 'Tutulo'
    logged_user = session.get('user')
    return render_template('home.html', title=title, logged_user=logged_user)

if __name__ == '__main__':
    app.run()
