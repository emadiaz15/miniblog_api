from flask import request, jsonify, Blueprint
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (jwt_required, create_access_token, current_user)
from app import db, jwt  # Importa instancias de la base de datos y JWT
from app.schemas import user_schema  # Importa el esquema de usuario
from app.models import User  # Importa el modelo de usuario

bp = Blueprint('users', __name__)  # Crea un Blueprint llamado 'users'

# Funciones para el manejo de identidad y búsqueda de usuario para JWT
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

# Ruta para el registro de usuarios
@bp.route('/register', methods=['POST'])
def register():
    user_data = request.json
    try:
        user = user_schema.load(user_data)  # Carga los datos del usuario utilizando el esquema
        user.set_password(user_data['password'])  # Establece la contraseña en forma de hash
        db.session.add(user)
        db.session.commit()  # Guarda el usuario en la base de datos
        return jsonify({'message': 'User registered successfully'})
    except ValidationError as err:
        return jsonify(err.messages), 400  # Devuelve errores de validación
    except IntegrityError:
        db.session.rollback()  # Realiza un rollback en caso de error (por ejemplo, usuario o correo ya registrados)
        return jsonify({'message': 'Username or email already registered'}), 400

# Ruta para el inicio de sesión
@bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    # Obtiene el usuario de la base de datos
    user = User.query.filter_by(username=username).first()

    # Verifica el usuario y la contraseña
    if user and user.check_password(password):
        access_token = create_access_token(identity=user)  # Crea un token de acceso JWT
        return jsonify({'access_token': access_token})

    return jsonify({'message': 'Invalid username or password'}), 401

# Ruta de verificación protegida por JWT
@bp.route('/verify', methods=['GET'])
@jwt_required()  # Requiere autenticación JWT
def verify():
    return jsonify(message=f'Verify endpoint for {current_user.username}')  # Devuelve un mensaje con el nombre del usuario actual
