from flask.ext.sqlalchemy import SQLAlchemy
import hashlib
import json

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True


class User(BaseModel):
    """Model for users table"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    apple_id = db.Column(db.String(300))
    password = db.Column(db.String(300), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

    # Todo: make these whatever the type of the coordinate system is?
    work = db.Column(db.String)
    home = db.Column(db.String)
    school = db.Column(db.String)

    def __init__(self, apple_id, password, first_name, last_name, work, home, school):
        self.apple_id = apple_id
        self.password = hashlib.sha224(password).hexdigest()
        self.first_name = first_name
        self.last_name = last_name
        self.work = work
        self.home = home
        self.school = school

    def __repr__(self):
        return '<apple_id {0}, first_name {1}, last_name {2}, work {3}, home {4}, school {5}>'.\
            format(self.apple_id, self.first_name, self.last_name, self.work, self.home, self.school)

    def map(self):
        return {"apple_id": self.apple_id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "work": self.work,
                "home": self.home,
                "school": self.school}
