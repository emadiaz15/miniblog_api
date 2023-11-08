from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import current_user, jwt_required
from marshmallow import ValidationError

from app import db  # Importa la instancia de la base de datos
from app.schemas import post_schema  # Importa el esquema de post
from app.models import Post  # Importa el modelo de post

bp = Blueprint('posts', __name__)  # Crea un Blueprint llamado 'posts'

class PostAPI(MethodView):

    def get(self, post_id):
        post = Post.query.get(post_id)
        if not post:
            return jsonify(error=f'Post {post_id} not found.'), 404
        return post_schema.dump(post), 200

    @jwt_required()
    def post(self):
        ''' Crea una nueva publicación '''
        post_data = request.json
        if not post_data:
            return jsonify(error='Not input data provided.'), 400

        try:
            post = post_schema.load(post_data)  # Carga los datos de la publicación utilizando el esquema
            post.user_id = current_user.id  # Asigna el ID del usuario actual como propietario de la publicación
            db.session.add(post)  # Agrega la publicación a la sesión de la base de datos
            db.session.commit()  # Guarda la publicación en la base de datos
            return post_schema.dump(post), 201  # Devuelve la publicación creada en la respuesta
        except ValidationError as err:
            return jsonify(err.messages), 400  # Devuelve errores de validación en caso de problemas

    @jwt_required()
    def delete(self, post_id):
        ''' Elimina una publicación '''
        post = Post.query.get(post_id)
        if not post:
            return jsonify(error=f'Post {post_id} not found.'), 404

        # Verifica si el usuario actual es el propietario de la publicación
        if post.user_id != current_user.id:
            return jsonify(error='Forbidden'), 403

        db.session.delete(post)  # Elimina la publicación de la sesión de la base de datos
        db.session.commit()  # Confirma la eliminación en la base de datos

        return jsonify(message='Post delete sucesfully.'), 200  # Devuelve un mensaje de éxito

    @jwt_required()
    def put(self, post_id):
        ''' Actualiza una publicación '''
        post_data = request.json
        if not post_data:
            return jsonify(error='No input data provided.'), 400

        post = Post.query.get(post_id)
        if not post:
            return jsonify(error=f'Post {post_id} not found.'), 404

        # Verifica si el usuario actual es el propietario de la publicación
        if post.user_id != current_user.id:
            return jsonify(error='Forbidden'), 403

        try:
            updated_post = post_schema.load(post_data, instance=post, partial=True)  # Carga los datos actualizados de la publicación
            db.session.commit()  # Guarda los cambios en la base de datos
            return post_schema.dump(updated_post), 200  # Devuelve la publicación actualizada en la respuesta
        except ValidationError as err:
            return jsonify(err.messages), 400  # Devuelve errores de validación en caso de problemas

post_view = PostAPI.as_view('post_api')
bp.add_url_rule('/', view_func=post_view, methods=['POST',])  # Agrega una regla de ruta para la creación de publicaciones
bp.add_url_rule('/<int:post_id>/', view_func=post_view, methods=['GET', 'PUT', 'DELETE'])  # Agrega una regla de ruta para consultar, actualizar y eliminar publicaciones por su ID
