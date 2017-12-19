from flask import Flask, request, flash, jsonify, render_template, url_for, redirect, session
import json
import sys
import random
from sqlalchemy import exc
from flasgger import Swagger
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
import uuid

from models import db, User

app = Flask(__name__)
Swagger(app)
app.config.from_pyfile('config.py')
db.init_app(app)

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def validate_user(email, password):
    print "attempting to validate user {0}".format(email)
    user = User.query.filter(User.apple_id == email).first()

    if not user:
        flash("No user found with email!")
        #raise StandardError("No user found with email {0}!".format(email))
    if not user.is_valid_password(password):
        flash("Invalid password")
        #raise StandardError("Invalid password")
    return user
    


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        
        user = User.query.filter(User.apple_id == email).first()
        print user 
        if not user:
            print "no user"
            error = "No user was found with that email!"
        elif not user.is_valid_password(password):
            error = "Invalid password!"
        else:
            print "here"
            login_user(user)
            return redirect(url_for('dashboard'))
        # except:
        #     e = sys.exc_info()[0]
        #     print str(e)
        #     return render_template('error.html', error_string=e)
    print "rendering.."
    return render_template('login.html', error=error)

    


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
            login_user(user)
            return redirect(url_for('dashboard'))
        except:
            e = sys.exc_info()[0]
            print str(e)
            return render_template('error.html', error_string=str(e))

    return render_template('register.html')


@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html')




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
