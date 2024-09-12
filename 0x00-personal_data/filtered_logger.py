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


def get_logger() -> logging.Logger:
    """returns a logging.Logger object
    """
    user_data = logging.getLogger('user_data')
    logging.setLevel('logging.INFO')
    stream = logging.StreamHandler()
    stream.setFormatter(RedactingFormatter)
    return user_data


PII_FIELDS = ["name", "email", "phone", "ssn", "password"]
