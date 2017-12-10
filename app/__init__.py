from flask import Flask, request, jsonify
import json
import sys
import random
from sqlalchemy import exc
from flasgger import Swagger
from flasgger.utils import swag_from

from models import db, Resource

app = Flask(__name__)
Swagger(app)
app.config.from_pyfile('config.py')
db.init_app(app)


## Routes ##

@app.route('/')
def api_health():
    '''
    Health check
    ---
    tags:
      - health
    responses:
      '200':
        description: App is running
    '''
    # TODO: check if can ping db
    return 'Service running!', 200


@app.route('/users/register', methods=['POST'])
def api_register(name):
    '''
    Gets a resource
    ---
    tags:
      - Jacalloc API
    responses:
      '201':
        description: Profile created
    parameters:
      - in: path
        description: user name
        name: name
        required: true
        type: string
    '''
    pass




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')