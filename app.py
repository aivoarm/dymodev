from flask import Flask, request, jsonify, render_template, redirect
from werkzeug.utils import secure_filename
import os
import subprocess

from normalize import normalize_data
from load import load_data_into_database
import sqlite3

app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def home():
    # Connect to the SQLite database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Retrieve data from the database
    cursor.execute('SELECT data FROM normalized_data')
    rows = cursor.fetchall()
    data_list = [row[0] for row in rows]

    # Close the connection
    conn.close()

    # Get a list of file names in the "data" folder
    data_folder = os.path.join(app.root_path, 'data')
    filenames = [filename for filename in os.listdir(data_folder) if os.path.isfile(os.path.join(data_folder, filename))]

    # Pass the data to the template
    return render_template('index.html', data_list=data_list, filenames=filenames)

# Define a route for receiving the FTP data
@app.route('/', methods=['POST'])
def index():
    return jsonify({'message': 'Data uploaded successfully'})

@app.route('/upload', methods=['POST'])
def upload_data():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    file_path = os.path.join('data', filename)  # Path to the "data" folder

    # Save the uploaded file to the "data" folder
    uploaded_file.save(file_path)

    # Read and normalize the uploaded data
    with open(file_path, 'r') as file:
        data = file.read()
        normalized_data = normalize_data(data)

    # Load the normalized data into the database
    load_data_into_database(normalized_data)

    # Redirect to the home page
    return redirect('/')

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = os.path.join('data', filename)  # Path to the file in the "data" folder

    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'message': 'File deleted successfully'})
    else:
        return jsonify({'message': 'File not found'})

@app.route('/init')
def init():
    # Run the other Python file using subprocess
    subprocess.call(['python', 'init.py'])
    return redirect('/')

    
if __name__ == '__main__':
    app.run(debug=True)
