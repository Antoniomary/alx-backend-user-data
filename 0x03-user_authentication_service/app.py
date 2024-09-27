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

    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user_id)
        else:
            abort(403)

    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
