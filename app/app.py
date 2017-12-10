from flask import Flask, request, jsonify, render_template
import json
import sys
import random
from sqlalchemy import exc
from flasgger import Swagger

from models import db, User

app = Flask(__name__)
Swagger(app)
app.config.from_pyfile('config.py')
db.init_app(app)


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


@app.route('/register', methods=['POST'])
def api_register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')