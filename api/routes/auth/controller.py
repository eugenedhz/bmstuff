from app import app
from configs.constants import ADMIN
from flask import jsonify, request
from flask_jwt_extended import (
    jwt_required, create_access_token,
    create_refresh_token, get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies, get_jwt
)

from api.extensions import db
from api.models import User, Admin
from api.routes.auth.access_decorator import role_required
from api.error.error_template import ApiError
from api.routes.auth.schemas import LoginAndSignupSchema


@app.route('/signup', methods=['POST'])
def signup_admin_post():

    json = request.json
    LoginAndSignupSchema().validate(json)

    username = json.get('username')
    password = json.get('password')

    user = User.query.filter_by(username=username).first()

    if user is not None:
        raise ApiError('USER_ALREADY_EXISTS', status_code=409)


    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()

    userId = str(user.id)

    # creating access token with info of user id and admin rights and refresh token with info of user id
    # note that here we set `fresh=True` for access to endpoint `delete-account`
    # [DEPRECATED UNTIL PRODUCTION] User will have `fresh=False` parameter in token with accessing `signup` endpoint and `refresh` endpoint
    # so anyone who has fresh token could not do some crtitical things without fresh token, such as deleting an account
    access_token = create_access_token(identity=userId, additional_claims={ADMIN: False})
    refresh_token = create_refresh_token(identity=userId, additional_claims={ADMIN: False})

    response = jsonify(login=True, adminRights=False, id=userId)

    # setting access and refresh token in cookies
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response, 201


@app.route('/login', methods=['POST'])
def login_admin_post():

    json = request.json
    LoginAndSignupSchema().validate(json)
    username = json.get('username')
    password = json.get('password')

    user = User.query.filter_by(username = username).first()

    if user is None:
        raise ApiError('INVALID_LOGIN_OR_PASSWORD', status_code=409)

    authorized = user.verify_password(password)

    if not authorized:
        raise ApiError('INVALID_LOGIN_OR_PASSWORD', status_code=409)


    userId = str(user.id)

    # creating access token with info of user id and admin rights and refresh token with info of user id
    access_token = create_access_token(identity=userId, additional_claims={ADMIN: False})
    refresh_token = create_refresh_token(identity=userId, additional_claims={ADMIN: False})

    response = jsonify(login=True, adminRights=False, id=userId)

    # setting access and refresh token in cookies
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response, 201


# checks via @jwt_required decorator if user has access-token
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout_post():

    response = jsonify(logout=True)

    unset_jwt_cookies(response)

    return response


# checks via @jwt_required decorator if user has access-token
@app.route('/user', methods=['DELETE'])
@jwt_required()
def delete_user():

    claims = get_jwt()
    identity = get_jwt_identity()

    if claims[ADMIN]:
        raise ApiError('ONLY_FOR_USERS', 403)

    user = User.query.filter_by(id = identity).first()

    if user is None:
        raise ApiError('USER_DOESNT_EXIST', 409)

    db.session.delete(user)
    db.session.commit()

    response = jsonify(deleted_account=True, id=identity)
    unset_jwt_cookies(response)

    return response


# checks via @admin_required decorator if user has admin rights
@app.route('/admin', methods=['DELETE'])
@role_required(ADMIN)
def delete_admin():

    identity = get_jwt_identity()

    user = Admin.query.filter_by(id = identity).first()

    if user is None:
        raise ApiError('ADMIN_DOESNT_EXIST', 409)

    db.session.delete(user)
    db.session.commit()

    response = jsonify(deletedAdmin=True, id=identity)
    unset_jwt_cookies(response)

    return response


# We are using the `refresh=True` options in jwt_required to only allow
# refresh tokens to access this route.
@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():

    claims = get_jwt()
    identity = get_jwt_identity() # getting id of our user from the token
    adminRights = claims[ADMIN]

    access_token = create_access_token(identity=identity, additional_claims={ADMIN: adminRights})

    response = jsonify(refresh=True)
    set_access_cookies(response, access_token)

    return response


# checks via @jwt_required decorator if user has access-token
@app.route('/user/access', methods=['GET'])
@jwt_required()
def user_protected():

    claims = get_jwt()
    identity = get_jwt_identity()

    return jsonify(access='approved', id=identity, adminRights=claims[ADMIN])


# checks via @admin_required decorator if user has admin rights
@app.route('/admin/access', methods=['GET'])
@role_required(ADMIN)
def admin_protected():

    claims = get_jwt()
    identity = get_jwt_identity()

    return jsonify(access='approved', id=identity, adminRights=claims[ADMIN])


# # this decorator is mostly used for debugging
# # In that example we print all cookies provided in request before every request
# @app.before_request
# def before_request_func():
#     print(request.cookies)