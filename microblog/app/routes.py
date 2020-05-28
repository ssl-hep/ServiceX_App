from flask import render_template, flash, redirect,request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from app import app
#from app.forms import LoginForm
# for python code on button press
import requests
from minio import Minio
import tempfile
import pyarrow.parquet as pq
import json
import sys
import os
sys.path.append(os.path.realpath('..'))
from servicex.models import UserModel

@app.route('/')
@app.route('/index', methods=['GET','POST'])

def index():
	#form = LoginForm()
	return render_template('index.html', title='Home')

@app.route('/on_press',methods=['GET','POST'])

def on_press():
	servicex_endpoint = "http://localhost:5000/servicex"
	response = requests.post(servicex_endpoint+"/transformation", json={
        "did": "mc15_13TeV:mc15_13TeV.361106.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zee.merge.DAOD_STDM3.e3601_s2576_s2132_r6630_r6264_p2363_tid05630052_00",
        "columns": "Electrons.pt(), Electrons.eta(), Electrons.phi(), Electrons.e(), Muons.pt(), Muons.eta(), Muons.phi(), Muons.e()",
        "image": "sslhep/servicex-transformer:latest",
        "result-destination": "object-store",
        "result-format": "parquet",
        "chunk-size": 7000,
        "workers": 1
    })
	global status_endpoint
	print(response.json())
	request_id = response.json()["request_id"]
	status_endpoint = servicex_endpoint+"/transformation/{}/status".format(request_id)
	return str(status_endpoint)

@app.route('/status', methods=['GET','POST'])

def status():
	status = requests.get(status_endpoint).json()
	print("We have processed {} files there are {} remainng".format(status['files-processed'], status['files-remaining']))
	return str(status)

@app.route('/acceptu', methods=['GET','POST'])

def acceptu():
	acceptu_endpoint = "http://localhost:5000/accept"
	print(str(request.form.to_dict()))
	print(str(request.form.items()))
	response = requests.post(acceptu_endpoint, data = json.dumps({"username":request.form.items().key}),  headers={"Authorization" :request.form.items().key})
	print(response.json())
	return str(acceptu_endpoint)
	#str(response)
@app.route('/new', methods=['GET','POST'])
def new():
	return render_template('new.html',
                           users=UserModel.query.all(),
                           title="Show Users")
