#!/usr/bin/env python3
"""
contains functionalities for authentication
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """converts a str to a hashed byte and returns it
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
