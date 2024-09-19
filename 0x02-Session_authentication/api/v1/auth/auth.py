#!/usr/bin/env python3
"""
contains the auth class
"""
import os
from flask import request
from typing import List, TypeVar


class Auth():
    """
    manages the API authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Defines routes that do not need authentication
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path in excluded_paths or path + '/' in excluded_paths:
            return False

        path_len = len(path)
        for excluded in excluded_paths:
            if excluded[-1] == '*':
                if path.startswith(excluded[:-1]):
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        validate requests to secure the API
        """
        if request is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        simply returns None
        """
        return None

    def session_cookie(self, request=None):
        """
        returns a cookie value from a request
        """
        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME')
        cookie = request.cookies.get(session_name)

        return cookie
