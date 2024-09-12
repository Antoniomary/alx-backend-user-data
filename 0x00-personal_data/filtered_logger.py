#!/usr/bin/env python3
"""
contains the function filter_datum
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

    def __init__(self, fields):
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
