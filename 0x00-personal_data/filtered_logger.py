#!/usr/bin/env python3
"""
contains classes and functions for user-data management
"""
from typing import List
import re
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """constructor
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum
        """
        record.msg = filter_datum(list(self.fields), self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """
    returns a log message obfuscated
    """
    for field in fields:
        pattern = "({}.)(.*?)({})".format(field, separator)
        message = re.sub(pattern, f"\\1{redaction}\\3", message)
    return message


PII_FIELDS = ["name", "email", "phone", "ssn", "password"]


def get_logger() -> logging.Logger:
    """returns a logging.Logger object
    """
    # Create (or get if it exists) the 'user_data' logger
    user_data = logging.getLogger('user_data')

    # Set the logger level
    user_data.setLevel(logging.INFO)

    # Does not propagate messages to other loggers
    user_data.propagate = False

    # Create a stream handler
    stream = logging.StreamHandler()

    # Instantiate RedactingFormatter with necessary fields
    formatter = RedactingFormatter(PII_FIELDS)

    # Set the formatter for the handler
    stream.setFormatter(formatter)

    # Add the handler to the logger
    user_data.addHandler(stream)

    return user_data
