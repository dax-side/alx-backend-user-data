#!/usr/bin/env python3
""" Personal data project """
import re
import os
import mysql.connector
import logging
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """ returns the log message obfuscated """
    for i in fields:
        message = re.sub(fr'{i}=.+?{separator}',
                         f'{i}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ constructor method """
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ filter values in a log record"""
        return filter_datum(self.fields,
                            self.REDACTION,
                            super().format(record),
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """ return logging.Logger object """
    obj = logging.getLogger("user_data")
    obj.setLevel(logging.INFO)
    obj.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    obj.addHandler(handler)
    return obj


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ return the connector of the database """
    user_name = os.getenv('PERSONAL_DATA_DB_USERNAME')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    return mysql.connector.connect(user=user_name,
                                   password=password,
                                   host=host,
                                   database=db_name)


def main():
    """ main function """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * from users")
    fields = [user[0] for user in cursor.description]
    print(fields)

    logger = get_logger()

    for i in cursor:
        list_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(i, fields))
        logger.info(i)

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
