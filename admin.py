from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from faker import Faker
import re  # Assuming this package exists, or you can write your own

import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)  # Change origins as needed # Change origins as needed

faker = Faker()

class Admin(AdminMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    user = db.relationship('User', backref='admin', lazy=True)
    
    def __init__(self, email, password):
        self.email = email
        self.password = password
        
class AdminSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'password')
        ordered = True

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    
    def __init__(self, email, password, admin_id):
        self.email = email
        self.password = password
        self.admin_id = admin_id
        
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'password', 'admin_id')
        ordered = True
        
user_schema = UserSchema()
multiple_user_schema = UserSchema(many=True)

admin_schema = AdminSchema()
multiple_admin_schema = AdminSchema(many=True)

@app.route('/user', methods=['POST'])
def add_user():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    admin_id = request.json.get('admin_id', None)

    if not validate_email(email):
        return make_response(jsonify({"message": "Invalid email"}), 400)

    if len(password) < 8:
        return make_response(jsonify({"message": "Password must be at least 8 characters long"}), 400)

    new_user = User(email, password, admin_id)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    return multiple_user_schema.jsonify(users)

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return make_response(jsonify({"message": "User not found"}), 404)

    db.session.delete(user)
    db.session.commit()
    return {'message': 'User deleted successfully'}

@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return make_response(jsonify({"message": "User not found"}), 404)

    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not validate_email(email):
        return make_response(jsonify({"message": "Invalid email"}), 400)

    if len(password) < 8:
        return make_response(jsonify({"message": "Password must be at least 8 characters long"}), 400)

    user.email = email
    user.password = password
    db.session.commit()

    return user_schema.jsonify(user)

@app.route('/admin', methods=['POST'])
def add_admin():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not validate_email(email):
        return make_response(jsonify({"message": "Invalid email"}), 400)

    if len(password) < 8:
        return make_response(jsonify({"message": "Password must be at least 8 characters long"}), 400)

    new_admin = Admin(email, password)
    db.session.add(new_admin)
    db.session.commit()

    return admin_schema.jsonify(new_admin)

@app.route('/admin', methods=['GET'])
def get_admins():
    admins = Admin.query.all()
    return multiple_admin_schema.jsonify(admins)

@app.route('/admin/<int:id>', methods=['DELETE'])
def delete_admin(id):
    admin = Admin.query.get(id)
    if not admin:
        return make_response(jsonify({"message": "Admin not found"}), 404)

    db.session.delete(admin)
    db.session.commit()
    return {'message': 'Admin deleted successfully'}

@app.route('/admin/<int:id>', methods=['PUT'])
def update_admin(id):
    admin = Admin.query.get(id)
    if not admin:
        return make_response(jsonify({"message": "Admin not found"}), 404)

    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not validate_email(email):
        return make_response(jsonify({"message": "Invalid email"}), 400)

    if len(password) < 8:
        return make_response(jsonify({"message": "Password must be at least 8 characters long"}), 400)

    admin.email = email
    admin.password = password
    db.session.commit()

    return admin_schema.jsonify(admin)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    # app.run(debug=True, host='127.0.0.1', port=5000)
    
def validate_email(email):
    # Assuming this function exists
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

# The above code is a complete example of how to use Flask, SQLAlchemy, Marshmallow, and Faker to create a REST API for a simple user and admin system.
# https://flask.palletsprojects.com/en/1.1.x/quickstart
# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlalchemy
# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlalchemy/#declarative
# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlalchemy/#association-object
# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlalchemy/#association-proxy
# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlalchemy/#declarative-mixins
