#!/usr/bin/python3
import mysql.connector
import csv
import uuid

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"

def connect_db():
    """Connect to MySQL server (no database specified)."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_database(connection):
    """Create the ALX_prodev database if it doesn't exist."""
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
    cursor.close()

def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to {DB_NAME}: {e}")
        return None

def create_table(connection):
    """Create the user_data table if it doesn't exist."""
    cursor = connection.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX idx_user_id(user_id)
        );
    """)
    cursor.close()
    print(f"Table {TABLE_NAME} created successfully")

def insert_data(connection, csv_file):
    """Insert data from CSV into the user_data table if it doesn't exist."""
    cursor = connection.cursor()
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_id = row.get('user_id') or str(uuid.uuid4())
            name = row['name']
            email = row['email']
            age = row['age']
            cursor.execute(f"""
                INSERT IGNORE INTO {TABLE_NAME} (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (user_id, name, email, age))
    connection.commit()
    cursor.close()

def stream_rows(connection):
    """Generator that streams rows one by one from the user_data table."""
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME};")
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield row
    cursor.close()
