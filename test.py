# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
# from flask_cors import CORS
# from faker import Faker

# import os

# app = Flask(__name__)

# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# db = SQLAlchemy(app)
# ma = Marshmallow(app)
# CORS(app)

# faker = Faker()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     email = db.Column(db.String, unique = True, nullable = False)
#     password = db.Column(db.String, nullable = False)

#     def __init__(self, email, password):
#         self.email = email
#         self.password = password



# class UserSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'email', 'password')
#         ordered = True
        
# user_schema = UserSchema()
# miltiple_user_schema = UserSchema(many = True)


# # /////////ADD-User-Endpoint//////////////////////////////////////////////////

# @app.route('/user', methods = ['POST'])

# def add_user():
#     email = request.json['email']
#     password = request.json['password']

#     new_user = User(email, password)

#     db.session.add(new_user)
#     db.session.commit()

#     return user_schema.jsonify(new_user)

# # /////////GET-User-Endpoint//////////////////////////////////////////////////

# @app.route('/user', methods = ['GET'])

# def get_user():
#     users = User.query.all()
#     return miltiple_user_schema.jsonify(users)

# # /////////DELETE-User-Endpoint//////////////////////////////////////////////////

# @app.route('/user/<int:id>', methods = ['DELETE'])

# def delete_user(id):
#     user = User.query.get(id)
#     db.session.delete(user)
#     db.session.commit()
#     return {'message': 'User deleted successfully'}

# # /////////UPDATE-User-Endpoint//////////////////////////////////////////////////

# @app.route('/user/<int:id>', methods = ['PUT'])

# def update_user(id):
#     user = User.query.get(id)
#     user.email = request.json['email']
#     user.password = request.json['password']

#     db.session.commit()
#     return user_schema.jsonify(user)

# # /////////Faker//////////////////////////////////////////////////
# @app.route('/populate_users', methods=['GET'])
# def populate_users():
#     num_users = 10  # Number of fake users to add
#     for _ in range(num_users):
#         fake_email = faker.email()
#         fake_password = faker.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
#         new_user = User(fake_email, fake_password)
#         db.session.add(new_user)
#     db.session.commit()
#     return {'message': f'Successfully added {num_users} fake users'}

# # /////////Run-App//////////////////////////////////////////////////

# if __name__ == '__main__':
#     host = '127.0.0.1'
#     port = 5000
#     for rule in app.url_map.iter_rules():
#         print(f"HTTP Endpoint: http://{host}:{port}{rule}")

#     with app.app_context():
#         db.create_all()
    
#     app.run(debug=True, host='127.0.0.1', port=5000)