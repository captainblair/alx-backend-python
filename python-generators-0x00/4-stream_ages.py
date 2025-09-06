#!/usr/bin/python3
seed = __import__('seed')

def stream_user_ages():
    """Generator that yields ages from the user_data table one by one"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row['age']  # yield one age at a time
    cursor.close()
    connection.close()

def average_age():
    """Calculate average age using the generator"""
    total = 0
    count = 0
    for age in stream_user_ages():  # loop over generator
        total += age
        count += 1
    if count == 0:
        return 0
    return total / count

if __name__ == "__main__":
    avg = average_age()
    print(f"Average age of users: {avg}")
