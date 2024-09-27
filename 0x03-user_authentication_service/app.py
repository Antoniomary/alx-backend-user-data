#!/usr/bin/env python3
"""
a flask app
"""
from auth import Auth
from flask import (
    abort,
    Flask,
    jsonify,
    make_response,
    redirect,
    request
)


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index() -> dict:
    """return a JSON payload of the form
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def create_user() -> dict:
    """registers a user
    """
    email = request.form.get('email')
    passwd = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"})
    if not passwd:
        return jsonify({"error": "password missing"})

    try:
        AUTH.register_user(email, passwd)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": email, "message": "user created"})


@app.route("/sessions", methods=["POST"])
def login():
    """logins user in
    """
    email = request.form.get('email')
    passwd = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"})
    if not passwd:
        return jsonify({"error": "password missing"})

    is_valid = AUTH.valid_login(email, passwd)
    if not is_valid:
        abort(401)

    session_id = AUTH.create_session(email)

    resp = make_response(jsonify({"email": email, "message": "logged in"}))
    resp.set_cookie("session_id", session_id)

    return resp


@app.route("/sessions", methods=["DELETE"])
def logout():
    """logouts a user
    """
    session_id = request.cookies.get("session_id")

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect('/')


@app.route("/profile")
def profile():
    """shows a user's profile
    """
    session_id = request.cookies.get("session_id")

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """resets a user's password
    """
    email = request.form.get('email')

    token = None

    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": token})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
