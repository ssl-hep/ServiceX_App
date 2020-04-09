from servicex.__init__ import app
from flask import jsonify


@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})
