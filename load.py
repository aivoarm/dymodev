import sqlite3

def load_data_into_database(data):
    # Connect to the SQLite database
    conn = sqlite3.connect('database.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS normalized_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT
        )
    ''')

    # Insert the normalized data into the database
    cursor.execute('INSERT INTO normalized_data (data) VALUES (?)', (data,))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
