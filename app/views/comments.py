from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, current_user
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from app import db  # Importa la instancia de la base de datos
from app.schemas import comment_schema  # Importa el esquema de comentario
from app.models import Comment  # Importa el modelo de comentario

bp = Blueprint('comments', __name__)  # Crea un Blueprint llamado 'comments'

class CommentAPI(MethodView):

    def get(self, comment_id):
        # Devuelve un comentario individual
        comment = Comment.query.get(comment_id)
        if not comment:
            return jsonify(error=f'Comment {comment_id} not found.'), 404
        return comment_schema.dump(comment), 200

    @jwt_required()
    def post(self):
        # Crea un nuevo comentario para una publicación específica
        comment_data = request.json
        if not comment_data:
            return jsonify(error=f'Not input data provided.'), 404

        try:
            new_comment = comment_schema.load(comment_data)  # Carga los datos del comentario utilizando el esquema
            new_comment.user_id = current_user.id  # Asigna el ID del usuario actual como propietario del comentario
            db.session.add(new_comment)  # Agrega el comentario a la sesión de la base de datos
            db.session.commit()  # Guarda el comentario en la base de datos
            return comment_schema.dump(new_comment), 201  # Devuelve el comentario creado en la respuesta (201 Created)
        except ValidationError as err:
            return jsonify(err.messages), 400
        except IntegrityError:
            db.session.rollback()  # Rollback en caso de error
            return jsonify(error=f'Error creating comment'), 400

    @jwt_required()
    def delete(self, comment_id):
        # Elimina un comentario individual
        comment = Comment.query.get(comment_id)
        if not comment:
            return jsonify(error=f'Comment {comment_id} not found.'), 404

        # Verifica si el usuario actual es el propietario del comentario
        if comment.user_id != current_user.id:
            return jsonify(error='Forbidden'), 403

        db.session.delete(comment)  # Elimina el comentario de la sesión de la base de datos
        db.session.commit()  # Confirma la eliminación en la base de datos

        return jsonify(message='Comment delete sucesfully.'), 200  # Devuelve un mensaje de éxito

    @jwt_required()
    def put(self, comment_id):
        # Actualiza un comentario individual
        comment_data = request.json
        if not comment_data:
            return jsonify(error='No input data provided.'), 400

        comment = Comment.query.get(comment_id)
        if not comment:
            return jsonify(error=f'Comment {comment_id} not found.'), 404

        # Verifica si el usuario actual es el propietario del comentario
        if comment.user_id != current_user.id:
            return jsonify(error='Forbidden'), 403

        try:
            updated_comment = comment_schema.load(comment_data, instance=comment, partial=True)  # Carga los datos actualizados del comentario
            db.session.commit()  # Guarda los cambios en la base de datos
            return comment_schema.dump(updated_comment), 200  # Devuelve el comentario actualizado en la respuesta
        except ValidationError as err:
            return jsonify(err.messages), 400

comment_view = CommentAPI.as_view('comment_api')
bp.add_url_rule('/', view_func=comment_view, methods=['POST',])  # Agrega una regla de ruta para la creación de comentarios
bp.add_url_rule('/<int:comment_id>', view_func=comment_view, methods=['GET', 'PUT', 'DELETE'])  # Agrega una regla de ruta para consultar, actualizar y eliminar comentarios por su ID
