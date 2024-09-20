#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def user_login() -> str:
    """ POST /api/v1//auth_session/login
    JSON body:
      - email
      - password
    Return:
      - User object JSON represented
      - 400 if can't login user
    """
    email = None
    password = None

    try:
        email = request.form.get("email")
        password = request.form.get("password")
    except Exception as e:
        return jsonify({"error": "Can't login user"}), 400

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({"email": email})
        if not users:
            return jsonify({"error": "no user found for this email"}), 404

        for user in users:
            if user.is_valid_password(password):
                from api.v1.app import auth
                session_id = auth.create_session(user.id)
                response = jsonify(user.to_json())
                session_name = getenv('SESSION_NAME')
                response.set_cookie(session_name, session_id)
                return response

        return jsonify({"error": "wrong password"}), 401
    except Exception as e:
        pass

    return jsonify({"error": "Can't login user"}), 400


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """ POST /api/v1//auth_session/logout
    Return:
        - empty json if logged out
        - 404 if not
    """
    from api.v1.app import auth

    is_destroyed = auth.destroy_session(request)
    if is_destroyed:
        return jsonify({}), 200

    abort(404)

