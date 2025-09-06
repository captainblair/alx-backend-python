# 0x00. Python - MySQL Generator

## Objective
Create a Python generator that streams rows from an SQL database one by one.

## Files
- `seed.py` – contains all functions to connect to MySQL, create database, create table, insert data, and a generator function to stream rows.
- `0-main.py` – tests the seed.py functions.
- `user_data.csv` – sample data to populate the database.

## Database
- MySQL database: `ALX_prodev`
- Table: `user_data`
  - Columns:
    - `user_id` (Primary Key, UUID, Indexed)
    - `name` (VARCHAR, NOT NULL)
    - `email` (VARCHAR, NOT NULL)
    - `age` (DECIMAL, NOT NULL)

## Usage
```bash
$ ./0-main.py
connection successful
Table user_data created successfully
Database ALX_prodev is present
[('UUID1', 'Name1', 'email1', 25), ...]
