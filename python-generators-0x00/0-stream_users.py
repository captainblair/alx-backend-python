#!/usr/bin/python3
import mysql.connector
from seed import connect_to_prodev

def stream_users():
    """Generator function that streams rows from user_data table one by one."""
    connection = connect_to_prodev()  # connect to ALX_prodev database
    cursor = connection.cursor(dictionary=True)  # fetch rows as dictionaries

    cursor.execute("SELECT * FROM user_data")  # query all rows

    for row in cursor:  # only 1 loop allowed
        yield row  # yield one row at a time

    cursor.close()
    connection.close()
