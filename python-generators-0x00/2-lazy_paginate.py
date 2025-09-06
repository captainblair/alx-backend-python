#!/usr/bin/python3
seed = __import__('seed')


def paginate_users(page_size, offset):
    """Fetch a single page of users from the database."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows  # This is fine here; it's a single page


def lazy_pagination(page_size):
    """Generator that lazily yields pages one by one."""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:  # no more rows
            break
        yield page  # yield one page at a time
        offset += page_size
