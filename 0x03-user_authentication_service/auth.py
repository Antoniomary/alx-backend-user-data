#!/usr/bin/env python3
"""
contains functionalities for authentication
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers a new user and returns the User object
        """
        user = None

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            pass

        if user:
            raise ValueError('User {} already exists'.format(email))

        hash_pwd = _hash_password(password)

        return self._db.add_user(email, hash_pwd)


def _hash_password(password: str) -> bytes:
    """converts a str to a hashed byte and returns it
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
