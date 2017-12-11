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


@app.route('/registerPage')
def show_register_page():
    return render_template('register.html')


@app.route('/registerUser', methods=['POST'])
def register_user():
    user = User(apple_id=request.form['email'],
                first_name=request.form['first-name'],
                last_name=request.form['last-name'],
                password=request.form['password'],
                work=request.form['work'],
                home=request.form['home'],
                school=request.form['school'])

    try:
        db.session.add(user)
        db.session.commit()
        return "Success!", 201
    except:
        e = sys.exc_info()[0]
        return str(e), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')