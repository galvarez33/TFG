from flask import Blueprint, render_template, session
from . import home_bp 

@home_bp.route('/')
def home():
    logged_user = session.get('logged_user')
    return render_template('home.html', logged_user=logged_user)
