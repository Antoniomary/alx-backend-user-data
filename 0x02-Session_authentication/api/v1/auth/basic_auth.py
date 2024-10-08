#!/usr/bin/env python3
"""
contains the BasicAuth class
"""
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
    manages the API authentication using Basic Authentication.
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        returns the Base64 part of the Authorization header
        for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
            ) -> str:
        """
        returns the decoded value of a
        Base64 string base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            ret = base64.b64decode(base64_authorization_header)
            return ret.decode('utf-8')
        except Exception:
            pass

        return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> (str, str):
        """
        returns the user email and password from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
            ) -> TypeVar('User'):
        """
        returns the User instance based on his email and password
        """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None

        try:
            for user in User.search({'email': user_email}):
                if user.is_valid_password(user_pwd):
                    return user
        except Exception:
            pass

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        overloads Auth and retrieves the User instance for a request
        """
        data = self.authorization_header(request)
        if data:
            detail = self.extract_base64_authorization_header(data)
            if detail:
                clear_detail = self.decode_base64_authorization_header(detail)
                if clear_detail:
                    credential = self.extract_user_credentials(clear_detail)
                    if credential:
                        user, pwd = credential[0], credential[1]
                        return self.user_object_from_credentials(user, pwd)
        return None
