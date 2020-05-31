from flask import render_template, request
from app import app

import requests
import json

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Home')
