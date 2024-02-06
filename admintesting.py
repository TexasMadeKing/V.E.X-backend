from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

    def __init__(self, username, email, password, admin_id):
        self.username = username
        self.email = email
        self.password = password
        self.admin_id = admin_id
        
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password', 'admin_id')
        ordered = True
        
user_schema = UserSchema()
users_schema = UserSchema(many=True)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        
class AdminSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password')
        ordered = True
        
admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)

# Routes
# Create a User
@app.route('/user', methods=['POST'])
def add_user():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    admin_id = request.json['admin_id']

    new_user = User(username, email, password, admin_id)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

# Get All Users
@app.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

# Get Single User
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

# Update Single User
@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    admin_id = request.json['admin_id']

    user.username = username
    user.email = email
    user.password = password
    user.admin_id = admin_id

    db.session.commit()

    return user_schema.jsonify(user)

# Delete User
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)

# Create an Admin
@app.route('/admin', methods=['POST'])
def add_admin():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    new_admin = Admin(username, email, password)

    db.session.add(new_admin)
    db.session.commit()

    return admin_schema.jsonify(new_admin)

# Get All Admins
@app.route('/admin', methods=['GET'])
def get_admins():
    all_admins = Admin.query.all()
    result = admins_schema.dump(all_admins)
    return jsonify(result)

# Get Single Admin
@app.route('/admin/<id>', methods=['GET'])
def get_admin(id):
    admin = Admin.query.get(id)
    return admin_schema.jsonify(admin)

# Update Single Admin
@app.route('/admin/<id>', methods=['PUT'])
def update_admin(id):
    admin = Admin.query.get(id)
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    admin.username = username
    admin.email = email
    admin.password = password

    db.session.commit()

    return admin_schema.jsonify(admin)

# Delete Admin
@app.route('/admin/<id>', methods=['DELETE'])
def delete_admin(id):
    admin = Admin.query.get(id)
    db.session.delete(admin)
    db.session.commit()

    return admin_schema.jsonify(admin)

@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        return user_schema.jsonify(user)
    else:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    

@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    admin_id = request.json['admin_id']
    new_user = User(username, email, password, admin_id)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

# 404 Error
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

# 500 Error
@app.errorhandler(500)
def internal_server_error(e):
    return "<h1>500</h1><p>Internal Server Error</p>", 500



# Function to print all routes
def print_routes():
    print("Available routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule}")

# Run Server
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print_routes()
    app.run(debug=True)
