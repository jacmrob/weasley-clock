from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from random import SystemRandom
from backports.pbkdf2 import pbkdf2_hmac, compare_digest
import json
from flask.ext.login import UserMixin

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True


class User(UserMixin, BaseModel):
    """Model for users table"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    apple_id = db.Column(db.String(300), unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

    _password = db.Column(db.LargeBinary(120), nullable=False)
    _salt = db.Column(db.String(120))

    # Todo: make these whatever the type of the coordinate system is?
    work = db.Column(db.String)
    home = db.Column(db.String)
    school = db.Column(db.String)

    @hybrid_property
    def password(self):
        return self._password

    # In order to ensure that passwords are always stored
    # hashed and salted in our database we use a descriptor
    # here which will automatically hash our password
    # when we provide it (i. e. user.password = "12345")
    def set_password(self, value):
        # When a user is first created, give them a salt
        if self._salt is None:
            self._salt = bytes(SystemRandom().getrandbits(128))
        self._password = self._hash_password(value)

    def is_valid_password(self, password):
        """Ensure that the provided password is valid.

        We are using this instead of a ``sqlalchemy.types.TypeDecorator``
        (which would let us write ``User.password == password`` and have the incoming
        ``password`` be automatically hashed in a SQLAlchemy query)
        because ``compare_digest`` properly compares **all***
        the characters of the hash even when they do not match in order to
        avoid timing oracle side-channel attacks."""
        new_hash = self._hash_password(password)
        return compare_digest(new_hash, self._password)

    def _hash_password(self, password):
        pwd = password.encode("utf-8")
        salt = bytes(self._salt)
        buff = pbkdf2_hmac("sha512", pwd, salt, iterations=100000)
        return bytes(buff)

    def __init__(self, apple_id, password, first_name, last_name, work, home, school, active=True):
        self.apple_id = apple_id
        self.first_name = first_name
        self.last_name = last_name
        self.work = work
        self.home = home
        self.school = school
        self.set_password(password)
        self.is_active = active

    def __repr__(self):
        return '<apple_id {0}, first_name {1}, last_name {2}, work {3}, home {4}, school {5}>'.\
            format(self.apple_id, self.first_name, self.last_name, self.work, self.home, self.school)

    def map(self):
        return {"apple_id": self.apple_id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "password": self._password,
                "work": self.work,
                "home": self.home,
                "school": self.school}

    def is_active():
        return self.is_active


class UserLocations(BaseModel):
    __tablename__ = 'userLocations'
    id = db.Column(db.Integer, primary_key=True)
    apple_id = db.Column(db.String(300))
    device = db.Column(db.String(300))
    home = db.Column(db.Boolean)
    work = db.Column(db.Boolean)
    school = db.Column(db.Boolean)

    # TODO: add more clock hands

    def __init__(self, apple_id, device):
        self.apple_id = apple_id
        self.device = device
        self.home = False
        self.work = False
        self.school = False
