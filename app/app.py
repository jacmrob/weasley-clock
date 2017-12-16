from flask import Flask, request, flash, jsonify, render_template, url_for, redirect, session
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


def validate_user(email, password):
    user = User.query.filter(User.apple_id == email).one()

    if user is None:
        raise StandardError("No user found!")
    if not user.is_valid_password(password):
        raise StandardError("Invalid password")
    return user


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = validate_user(email, password)
            return redirect(url_for('dashboard', user=user.first_name))

        except:
            e = sys.exc_info()[0]
            print str(e)
            return str(e), 500
    return render_template('login.html')
    


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user = User(apple_id=request.form['email'],
                first_name=request.form['first-name'],
                last_name=request.form['last-name'],
                password=request.form['password'],
                work=request.form['work'],
                home=request.form['home'],
                school=request.form['school'])

        try:
            existing_user = User.query.filter(User.apple_id == user.apple_id).first()
            if existing_user is not None:
                raise StandardError("A user with that email already exists")

            db.session.add(user)
            db.session.commit()
            return redirect(url_for('dashboard', user=user.first_name))
        except:
            e = sys.exc_info()[0]
            print str(e)
            return str(e), 500

    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    # TODO: use flask-login
    return render_template('dashboard.html')




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
