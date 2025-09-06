#!/usr/bin/python3
import csv
import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator that yields rows from user_data table in batches"""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # replace with your password
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")

    batch = []
    for row in cursor:
        batch.append(row)
        if len(batch) == batch_size:
            for item in batch:
                yield item  # use yield, not return
            batch = []

    # Yield remaining rows if any
    for item in batch:
        yield item

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """Process each batch and filter users over age 25"""
    for user in stream_users_in_batches(batch_size):
        if user["age"] > 25:
            yield user  # again, yield to comply with generator
