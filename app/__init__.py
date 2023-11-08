from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from app.config import Settings  # Importa la configuración de la aplicación

app = Flask(__name__)  # Crea una instancia de la aplicación Flask
app.config.from_object(Settings)  # Configura la aplicación utilizando la configuración desde el objeto "Settings"

db = SQLAlchemy(app)  # Inicializa la extensión SQLAlchemy para interactuar con la base de datos
ma = Marshmallow(app)  # Inicializa la extensión Marshmallow para serialización/deserialización de datos
migrate = Migrate(app, db)  # Inicializa la extensión de migración para la base de datos
jwt = JWTManager(app)  # Inicializa la extensión de manejo de tokens JWT

# Define un endpoint en la raíz de la aplicación
@app.route('/')
def index():
    return jsonify(message='Hola, bienvenido a la efi de DevOps')

# Importa y registra las rutas definidas en otros archivos (users, posts, comments)
from app.views import users, posts, comments
app.register_blueprint(users.bp, url_prefix='/users')  # Registra las rutas relacionadas con usuarios
app.register_blueprint(posts.bp, url_prefix='/posts')  # Registra las rutas relacionadas con publicaciones
app.register_blueprint(comments.bp, url_prefix='/comments')  # Registra las rutas relacionadas con comentarios
