from datetime import datetime
from sqlalchemy import DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db  # Importa la instancia de SQLAlchemy

# User model
class User(db.Model):
    __tablename__ = 'users'  # Nombre de la tabla en la base de datos

    id = db.Column(db.Integer, primary_key=True)  # Campo de clave primaria
    username = db.Column(db.String(64), unique=True, nullable=False)  # Nombre de usuario
    email = db.Column(db.String(120), unique=True, nullable=False)  # Dirección de correo electrónico
    password_hash = db.Column(db.String(256), nullable=False)  # Hash de la contraseña
    created_at = db.Column(DateTime, default=datetime.utcnow)  # Fecha de creación
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Fecha de actualización

    def set_password(self, password):
        # Método para establecer la contraseña en forma de hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # Método para verificar si la contraseña ingresada coincide con la almacenada
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'  # Representación legible del modelo

# Post model
class Post(db.Model):
    __tablename__ = 'posts'  # Nombre de la tabla en la base de datos

    id = db.Column(db.Integer, primary_key=True)  # Campo de clave primaria
    title = db.Column(db.String(150), nullable=False)  # Título del post
    content = db.Column(db.Text, nullable=False)  # Contenido del post
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Clave externa para relacionar con usuarios
    created_at = db.Column(DateTime, default=datetime.utcnow)  # Fecha de creación
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Fecha de actualización
    comments = db.relationship('Comment', backref='post', lazy=True)  # Relación con comentarios

    def __repr__(self):
        return f'<Post {self.title}>'  # Representación legible del modelo

# Comment model
class Comment(db.Model):
    __tablename__ = 'comments'  # Nombre de la tabla en la base de datos

    id = db.Column(db.Integer, primary_key=True)  # Campo de clave primaria
    content = db.Column(db.Text, nullable=False)  # Contenido del comentario
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Clave externa para relacionar con usuarios
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)  # Clave externa para relacionar con posts
    created_at = db.Column(DateTime, default=datetime.utcnow)  # Fecha de creación
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Fecha de actualización

    def __repr__(self):
        return f'<Comment {self.id} by User {self.user_id}>'  # Representación legible del modelo
