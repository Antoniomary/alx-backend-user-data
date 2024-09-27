#!/usr/bin/env python3
"""
contains functionalities for authentication
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union


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

    def valid_login(self, email: str, password: str) -> bool:
        """checks user password
           if password is valid, returns True else False
        """
        user = None

        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            pass

        return False

    def create_session(self, email: str) -> str:
        """returns the session ID of a user based on the email passed
        """
        user = None

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return

        session_id = _generate_uuid()
        user.session_id = session_id

        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """returns the corresponding user of a session id if they exist
           else None
        """
        user = None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return

        return user

    def destroy_session(self, user_id: int) -> None:
        """updates the corresponding user’s session ID to None
        """
        user = None

        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
        except NoResultFound:
            pass

        return None

    def get_reset_password_token(self, email: str) -> str:
        """returns a reset_token for a user after resetting it
        """
        user = None

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        user.reset_token = reset_token

        return reset_token


def _hash_password(password: str) -> bytes:
    """converts a str to a hashed byte and returns it
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """return a string representation of a new UUID
    """
    return str(uuid.uuid4())
