#!/usr/bin/env python3
"""
contains the auth class
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """
    manages the API authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        simply returns False
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        simply returns None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        simply returns None
        """
        return None
