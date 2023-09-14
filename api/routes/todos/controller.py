from app import app
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.extensions import db
from api.models import Todo, User
from api.error.error_template import ApiError
from api.routes.todos.schemas import TodoSchema, TodoSchemaUpdate
from api.routes.todos.todos_to_json import todo_json


@app.route('/todo', methods=['POST'])
@jwt_required()
def make_todo():

    json = request.json
    TodoSchema().validate(json)

    user_id = get_jwt_identity()
    user_by_id = User.query.filter_by(id=user_id).first()

    todo = Todo(**json, user=user_by_id)

    db.session.add(todo)
    db.session.commit()

    return todo_json(todo, is_many=False, field_list=None), 201


@app.route('/todo/<int:id>', methods=['PATCH'])
@jwt_required()
def update_todo(todo_id):
    user_id = get_jwt_identity()

    

    db.session.commit()

    return todo_json(todo, is_many=False, field_list=None), 201