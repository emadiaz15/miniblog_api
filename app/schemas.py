# Importaciones necesarias
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app import ma  # Importa la instancia de Marshmallow
from app.models import User, Post, Comment  # Importa tus modelos de datos

# User Schemas
class UserSchema(ma.SQLAlchemyAutoSchema):
    # Definición de campos y configuraciones del esquema para el modelo User
    id = fields.String(dump_only=True)  # Campo "id" solo se usa en la salida (dump)
    created_at = fields.DateTime(dump_only=True)  # Campo "created_at" solo se usa en la salida (dump)
    updated_at = fields.DateTime(dump_only=True)  # Campo "updated_at" solo se usa en la salida (dump)
    password = fields.String(load_only=True)  # Campo "password" solo se usa para cargar datos

    class Meta:
        model = User  # Modelo asociado al esquema
        fields = ['id', 'username', 'email', 'password']  # Campos a incluir en la serialización
        load_instance = True  # Habilita la carga de objetos desde JSON

user_schema = UserSchema()  # Instancia de UserSchema para un solo objeto
users_schema = UserSchema(many=True)  # Instancia de UserSchema para varios objetos

# Post Schemas
class PostSchema(ma.SQLAlchemyAutoSchema):
    # Definición de campos y configuraciones del esquema para el modelo Post
    id = fields.String(dump_only=True)  # Campo "id" solo se usa en la salida (dump)
    comments = fields.Nested('CommentSchema', many=True, dump_only=True)  # Relacionado con el esquema de comentarios
    created_at = fields.DateTime(dump_only=True)  # Campo "created_at" solo se usa en la salida (dump)
    updated_at = fields.DateTime(dump_only=True)  # Campo "updated_at" solo se usa en la salida (dump)
    user_id = fields.String(dump_only=True)  # Campo "user_id" solo se usa en la salida (dump)

    class Meta:
        model = Post  # Modelo asociado al esquema
        fields = ['id', 'title', 'content', 'user_id', 'comments', 'created_at', 'updated_at']  # Campos a incluir en la serialización
        load_instance = True  # Habilita la carga de objetos desde JSON

post_schema = PostSchema()  # Instancia de PostSchema para un solo objeto
posts_schema = PostSchema(many=True)  # Instancia de PostSchema para varios objetos

# Comment Schemas
class CommentSchema(ma.SQLAlchemyAutoSchema):
    # Definición de campos y configuraciones del esquema para el modelo Comment
    id = fields.String(dump_only=True)  # Campo "id" solo se usa en la salida (dump)
    created_at = fields.DateTime(dump_only=True)  # Campo "created_at" solo se usa en la salida (dump)
    updated_at = fields.DateTime(dump_only=True)  # Campo "updated_at" solo se usa en la salida (dump)
    user_id = fields.String(dump_only=True)  # Campo "user_id" solo se usa en la salida (dump)

    class Meta:
        model = Comment  # Modelo asociado al esquema
        fields = ['id', 'content', 'user_id', 'post_id', 'created_at', 'updated_at']  # Campos a incluir en la serialización
        load_instance = True  # Habilita la carga de objetos desde JSON

comment_schema = CommentSchema()  # Instancia de CommentSchema para un solo objeto
comments_schema = CommentSchema(many=True)  # Instancia de CommentSchema para varios objetos
