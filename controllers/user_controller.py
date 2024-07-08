from flask import  Blueprint, jsonify,request  

import cloudinary.uploader

import bcrypt

from extensions import db, ma

from models.user_model import *

class UserSchema(ma.Schema):
    class Meta:
        fields=('id','first_name','last_name','phone','adress','email','username','password','image','role')


user_schema=UserSchema()            
users_schema=UserSchema(many=True)  

# Crear un Blueprint para la entidad User
user_bp = Blueprint('users', __name__)

# crea los endpoint o rutas (json)

#Obtener todos los usuarios
@user_bp.route('/users',methods=['GET'])
def get_users():
    all_users=User.query.all()         
    result=users_schema.dump(all_users)                                     
    return jsonify(result)                    

#obtener el usuario que recibo por id
@user_bp.route('/users/<id>',methods=['GET'])
def get_user(id):
    user=User.query.get(id)
    return user_schema.jsonify(user)   

#Borrar el usuario que recibo por id
@user_bp.route('/users/<id>',methods=['DELETE'])
def delete_user(id):
    user=User.query.get(id)
    db.session.delete(user)

# Agregar un nuevo Usuario
@user_bp.route('/users', methods=['POST'])
def add_user():
    data = request.form
    image = request.files.get('image')  # Usamos get para obtener la imagen sin error si no está presente

    password = data['password']
    confirm_password = data['confirm_password']

    if password != confirm_password:
        return jsonify({'Mensaje': 'Las contraseñas no coinciden'}), 400

    image_url = None
    if image:  # Verificar si se envió una imagen
        result = cloudinary.uploader.upload(image)
        image_url = result['secure_url']

    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        address=data['address'],
        email=data['email'],
        username=data['username'],
        password=hashed_password.decode('utf-8'),
        image=image_url,
        role='USER'
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'Mensaje': 'Registro exitoso!'})

#Actualizar un Usuario
@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'Mensaje': 'Usuario no encontrado'}), 404

    data = request.form

    if 'image' in request.files:
        image = request.files['image']
        result = cloudinary.uploader.upload(image)
        user.image = result['secure_url']

    if 'first_name' in data and user.first_name != data['first_name']:
        user.first_name = data['first_name']
    if 'last_name' in data and user.last_name != data['last_name']:
        user.last_name = data['last_name']
    if 'phone' in data and user.phone != data['phone']:
        user.phone = data['phone']
    if 'address' in data and user.address != data['address']:
        user.address = data['address']
    if 'email' in data and user.email != data['email']:
        user.email = data['email']
    if 'username' in data and user.username != data['username']:
        user.username = data['username']
    if 'password' in data and 'confirm_password' in data:
        if data['password'] != data['confirm_password']:
            return jsonify({'Mensaje': 'Las contraseñas no coinciden'}), 400
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        if user.password != hashed_password:
            user.password = hashed_password
    if 'role' in data and user.role != data['role']:
        user.role = data['role']

    db.session.commit()
    return jsonify({'Mensaje': 'Usuario actualizado exitosamente!'})

#Verificar Login
@user_bp.route('/login', methods=['POST'])
def login_user():
    data = request.json
    username_or_email = data.get('username_or_email')
    password = data.get('password')

    if not username_or_email or not password:
        return jsonify({'Mensaje': 'Falta el nombre de usuario o la contraseña'}), 400

    user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({'Mensaje': 'Credenciales inválidas'}), 401

    user_data = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone': user.phone,
        'address': user.address,
        'email': user.email,
        'username': user.username,
        'image': user.image,
        'role': user.role
    }

    return jsonify({'user': user_data})