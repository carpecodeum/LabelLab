from flask import jsonify

from api.extensions import db, ma
from api.models.User import User
from api.serializers.users import UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)
    
def to_json(self):
    """
    Returns a JSON object
    """
    return user_schema.jsonify(self)

def find_by_email(email):
    return User.query.filter_by(email=email).first()

def find_by_user_id(_id):
    return User.query.filter_by(id=_id).first()

def find_by_username(username):
    return User.query.filter_by(username=username).first()

def delete_by_id(_id):
    User.query.filter_by(id=_id).delete()
    db.session.commit()

def save(user):
    """
    Save a user to the database.
    This includes creating a new user and editing one.
    """
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user)