from flask import Blueprint, render_template, session,request
from . import home_bp 
import requests

@home_bp.route('/')
def home():
    logged_user = session.get('logged_user')
    return render_template('home.html', logged_user=logged_user)




