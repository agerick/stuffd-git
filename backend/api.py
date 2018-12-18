#!myvenv/bin/python
from flask import jsonify, abort, request, send_from_directory
from flask_cors import CORS
import json
import os
from flask_restful import Resource, Api
from models import *



cwd = os.getcwd()

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')
CORS(app)


with open('./data_json/products.json') as json_file:
    d = json.load(json_file)

@app.route('/products')
def get_products():
    return jsonify(d)




@app.route('/logo')
def send_logo():
    return send_from_directory(directory=cwd,filename='logo1.png')

# Basic route

@app.route('/hi')
def index():
	return "Hello, World"

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

######################################
if __name__=='__main__':
	app.run(debug=True)
