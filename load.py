import os
import sqlite3

def load_data_into_database():
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

    # Get a list of file names in the "data" folder
    data_folder = 'data'  # Change 'data' to the correct folder path if needed
    filenames = [filename for filename in os.listdir(data_folder) if os.path.isfile(os.path.join(data_folder, filename))]

    # Iterate through the files and insert data into the database
    for filename in filenames:
        with open(os.path.join(data_folder, filename), 'r') as file:
            data = file.read()

            # Check if the data already exists in the database
            cursor.execute('SELECT data FROM normalized_data WHERE data = ?', (data,))
            existing_data = cursor.fetchone()

            if existing_data:
                print(f"Data in file '{filename}' already exists in the database. Skipping...")
            else:
                # Insert the normalized data into the database
                cursor.execute('INSERT INTO normalized_data (data) VALUES (?)', (data,))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()




def cleanup_database():
    # Connect to the SQLite database
    conn = sqlite3.connect('database.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Drop the normalized_data table if it exists
    cursor.execute('DROP TABLE IF EXISTS normalized_data')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS normalized_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT
        )
    ''')
    # Commit the changes and close the connection
    conn.commit()
    conn.close()