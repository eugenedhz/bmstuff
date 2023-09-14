from app import app
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.extensions import db, jwt
from api.models import User
from api.error.error_template import ApiError
from api.routes.auth.schemas import LoginAndSignupSchema


@app.route('/user/info', methods=['GET'])
@jwt_required()
def get_user_info():

    user_id = get_jwt_identity()

    user = User.query.filter_by(id = user_id).first()

    return jsonify(id = user_id, username = user.username, email = user.email)
