#!/usr/bin/env python3
"""
Main file
"""
import requests


URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """registers a user
    """
    url = f"{BASE_URL}/users"
    payload = {"email": email, "password": password}

    response = requests.post(url, data=payload)

    # assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """logs user with wrong details
    """
    url = f"{BASE_URL}/sessions"
    payload = {"email": email, "password": password}

    response = requests.post(url, data=payload)

    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """logs in a user
    """
    url = f"{BASE_URL}/sessions"
    payload = {"email": email, "password": password}

    response = requests.post(url, data=payload)

    assert response.json() == {"email": email, "message": "logged in"}


def profile_unlogged() -> None:
    """valids a users session without session id
    """
    url = f"{BASE_URL}/profile"

    response = requests.get(url)

    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """valids a users session with session id
    """
    url = f"{BASE_URL}/profile"
    payload = {"session_id": session_id}

    response = requests.get(url, data=payload)

    assert response.json() == {"email": user.email}


def log_out(session_id: str) -> None:
    """logs user out
    """
    url = f"{BASE_URL}/sessions"
    payload = {"session_id": session_id}

    response = requests.delete(url, data=payload)

    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """resets password token of a user
    """
    url = f"{BASE_URL}/reset_password"
    payload = {"email": email}

    response = requests.post(url, data=payload)

    assert response.json() == {"email": email, "reset_token": token}


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """updates user's password
    """
    url = f"{BASE_URL}/reset_password"
    payload = {
        "email": email,
        "reset_token": reset_token,
        "new password": new_password,
    }

    response = requests.put(url, data=payload)

    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
