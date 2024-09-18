#!/usr/bin/env python3
"""
contains the BasicAuth class
"""
import base64
from api.v1.auth.auth import Auth


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
            base64_authorization_header = ret
        except Exception:
            return None

        return base64_authorization_header.decode('utf-8')
