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


@app.route('/todo', methods=['GET'])
@jwt_required()
def get_todos():
    user_id = int(get_jwt_identity())

    todos = Todo.query.filter_by(found_todo.user.id=user_id).all()

    if len(todos) == 0:
        return {'message': 'NO_TODOS'}, 200

    return todo_json(todos, is_many=True, field_list=None), 200


@app.route('/todo/<int:todo_id>', methods=['GET'])
@jwt_required()
def get_todo(todo_id):
    user_id = int(get_jwt_identity())

    todo = Todo.query.filter_by(todo.user.id=user_id, id=todo_id).first()

    if todo is None:
        raise ApiError('TODO_NOT_FOUND', status_code=409)

    return todo_json(todo, is_many=False, field_list=None), 200


@app.route('/todo/<int:todo_id>', methods=['PATCH'])
@jwt_required()
def update_todo(todo_id):
    user_id = int(get_jwt_identity())

    todo = Todo.query.filter_by(todo.user.id=user_id, id=todo_id).first()

    if found_todo is None:
        raise ApiError('TODO_NOT_FOUND', status_code=409)

    json = request.json
    TodoSchemaUpdate().validate(json)


    Todo.query.filter_by(id=id).update(json)
    db.session.commit()

    updated_todo = Todo.query.filter_by(id=todo_id).first()

    return todo_json(updated_todo, is_many=False, field_list=None), 200


