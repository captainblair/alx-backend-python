#!/usr/bin/python3
import csv
import mysql.connector
from seed import connect_to_prodev  # assuming seed.py is already set up

def stream_users_in_batches(batch_size):
    """Generator: fetch rows from user_data table in batches"""
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    offset = 0

    while True:
        cursor.execute(
            "SELECT * FROM user_data LIMIT %s OFFSET %s",
            (batch_size, offset)
        )
        batch = cursor.fetchall()
        if not batch:
            break
        for row in batch:
            yield row
        offset += batch_size

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """Process each batch to filter users over age 25"""
    for user in stream_users_in_batches(batch_size):
        if user['age'] > 25:
            print(user)
