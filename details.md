## ./1.brd.py

```python
brd = """

Building with chat GPT

Imagine you are a developer given requirements to build an application that can use secure ftp connection for data exchange, have capability to read data structured and semi structured data , load into SQLite tables, normalize data, have ability to merge tables  , perform calculations, give output as downloadable reports, have ability to configure business rules and apply them during etl. also want the ui be modern , simple and elegant  . 
Application Requirements:

Secure FTP Connection:

The application should support a secure FTP connection to facilitate data exchange with external systems securely.
Data Reading and Loading:

The application should be capable of reading both structured and semi-structured data from various file formats (e.g., CSV, XML, JSON, etc.).
The extracted data should be loaded into SQLite tables for further processing and analysis.
Data Normalization:

The application should have the ability to normalize the loaded data into appropriate table structures based on predefined data models or user-defined rules.
Normalization should ensure consistency, eliminate redundancy, and improve data integrity.
Table Merging:

The application should provide functionality to merge multiple SQLite tables based on specific criteria or relationships.
Merging tables should facilitate combining data from different sources to generate comprehensive datasets.
Calculations and Data Manipulation:

The application should support performing calculations and data manipulations on the loaded and merged data.
Users should be able to define custom calculations or apply built-in functions to derive new insights or transform the data.
Downloadable Reports:

The application should generate downloadable reports based on the processed and analyzed data.
Reports should be available in various formats (e.g., PDF, CSV, Excel, etc.) to cater to different user requirements.
Configuration of Business Rules:

The application should allow users to configure and manage business rules for the ETL (Extract, Transform, Load) process.
Business rules could include data validation, transformation logic, data filtering, and other rule-based operations.
Modern and Elegant UI:

The application's user interface (UI) should have a modern, simple, and elegant design.
The UI should provide an intuitive user experience, making it easy for users to navigate, configure, and interact 
"""```

## ./normalize.py

```python
import csv
import json
import xml.etree.ElementTree as ET

import csv

def normalize_data(data, file_format):
    normalized_data = ""

    if file_format == "csv":
        # Parse CSV data
        reader = csv.reader(data.splitlines())
        rows = list(reader)

        # Normalize CSV data
        # Perform your normalization operations on the rows

        # Convert the normalized data back to CSV format
        normalized_rows = []
        for row in rows:
            normalized_row = [str(cell).lower() for cell in row]  # Convert all cells to lowercase strings
            normalized_rows.append(normalized_row)
        
        normalized_data = "\n".join([",".join(row) for row in normalized_rows])

    return normalized_data

```

## ./pushtogithub.py

```python
import subprocess

# Run 'git add .' command
subprocess.run(['git', 'add', '.'])

# Run 'git commit -m "update"' command
subprocess.run(['git', 'commit', '-m', 'update'])

# Run 'git push remote main' command
subprocess.run(['git', 'push', 'origin', 'main'])
```

## ./app.py

```python
from flask import Flask, request, jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
import subprocess

from normalize import normalize_data
from load import load_data_into_database, cleanup_database
import sqlite3

app = Flask(__name__)

# Define a route for the home page


@app.route('/')
def home():
    # Check if the database file exists
    if not os.path.exists('database.db'):
        return render_template('index.html', data_list=["data_list"], filenames=["placeholder   "])

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


@app.route('/push-git')
def pushgit():
    # Run the other Python file using subprocess
    subprocess.call(['python', 'pushtogithub.py'])
    return redirect('/')

@app.route('/load')
def load():
    cleanup_database()
    # Run the other Python file using subprocess
    load_data_into_database()
   
    return redirect(url_for('index'))



@app.route('/normalize', methods=['POST'])
def normalize():
        # Get a list of file names in the "data" folder
    data_folder = 'data'  # Change 'data' to the correct folder path if needed
    filenames = [filename for filename in os.listdir(data_folder) if os.path.isfile(os.path.join(data_folder, filename))]

    # Iterate through the files and insert data into the database
    for filename in filenames:
        
        filename = request.form.get('filename')

    # Perform the normalization logic here using the filename

    # Example normalization code (replace with your actual implementation)
        normalized_data = normalize_data(filename, file_format="csv")

        if normalized_data:
            # Normalization successful
            return jsonify({'success': True, 'normalized_data': normalized_data})
        else:
            # Normalization failed
            return jsonify({'success': False})

def normalize_data(filename, file_format):
    # Implement your actual normalization logic here
    # You can use the provided `normalize_data` function in your question as a starting point
    
    # Placeholder code that simply returns the filename for demonstration purposes
    filename="n_"+filename
    return filename

if __name__ == '__main__':
    app.run(debug=True)
```

## ./process.py

```python
```

## ./init.py

```python
import os
import fnmatch

def ignore_patterns(filename, patterns):
    return any(fnmatch.fnmatch(filename, pattern) for pattern in patterns)

def save_directory_structure(root_dir, ignored_patterns, output_file):
    with open(output_file, 'w') as file:
        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if not ignore_patterns(d, ignored_patterns)]
            files[:] = [f for f in files if not ignore_patterns(f, ignored_patterns)]
            
            relative_path = os.path.relpath(root, root_dir)
            
            for file_name in files:
                file.write(os.path.join(relative_path, file_name) + '\n')

ignored_patterns = [
    '*.pyc',
    '*.log',
    '*.db',
    '.env',
    'secret.txt',
    'database.db',
    '.gitignore',
    '*.idea',
    '*.iml',
    '*.vscode',
    '__pycache__',
    'myenv',
    'data*',
    '.git',
    '*txt',
    '*md'
]

project_directory = os.path.dirname(os.path.abspath(__file__))
output_file = 'structure.txt'

save_directory_structure(project_directory, ignored_patterns, output_file)

# Open the file in read mode
# Step 1: Open the file
with open('structure.txt', 'r') as file:
    # Step 2: Read the contents of the file
    lines = file.readlines()

# Step 3: Close the file (automatically handled by 'with' statement)

# Step 4: Store the data in an array
file_list = [line.strip() for line in lines]


with open("details.md", "w") as file:
    for file_path in file_list:
        with open(file_path, "r") as f:
            content = f.read()
            file.write(f"## {file_path}\n\n")
            file.write("```python\n")
            file.write(content)
            file.write("```\n\n")
```

## ./load.py

```python
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
    conn.close()```

## templates/index.html

```python
<!DOCTYPE html>
<html>

<head>
    <title>The App</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
    <style>
        body {
            background-color: #f8f9fa;
            font-family: Arial, sans-serif;
            padding: 20px;
        }

        .container {
            max-width: auto;
            margin: 0 auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        h1 {
            text-align: center;
            margin-bottom: 30px;
        }

        .btn {
            width: 100%;
            margin-top: 20px;
        }

        .file-list {
            list-style: none;
            padding: 0;
        }

        .file-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }

        .file-item .file-name {
            flex-grow: 1;
        }

        .file-item .file-delete {
            margin-left: 10px;
            color: red;
            cursor: pointer;
        }

        .file-normalize {
            margin-left: 10px;
            color: rgb(0, 38, 255);
            cursor: pointer;
        }

        table {
            border-collapse: collapse;
            width: 100%;
        }

        th,
        td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }

    </style>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>

<body>
    <div class="container">
        <h1>The App</h1>

        <form action="/upload" method="post" enctype="multipart/form-data">
            <div class="form-group">
                <input type="file" name="file" class="form-control-file" required>
            </div>
            <button type="submit" class="btn btn-primary">Upload Data</button>
        </form>

        <h2>File List:</h2>
        <ul class="file-list">
            {% for filename in filenames %}
            <li class="file-item">
                <span class="file-name">{{ filename }}</span>
                <span class="file-normalize">Normalize</span>
                <span class="file-delete">Delete</span>
            </li>
            {% endfor %}
        </ul>

        <button class="btn btn-primary" id="load-data">Load Data</button>
        <button class="btn btn-primary" id="run-init">Run /init</button>
        <button class="btn btn-primary" id="push-git">push to github</button>


        <div class="container">
            <table id="data-table">
                <thead>
                    <tr>
                        {% for header in data_list[0].split(',') %}
                        <th>{{ header }}</th>
                        {% endfor %}
                    </tr>
                </thead>
                <tbody>
                    {% for row in data_list[1:] %}
                    <tr>
                        {% for cell in row.split(',') %}
                        <td>{{ cell }}</td>
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

    <script>
        $(document).ready(function () {
            // Delete file
            $('.file-delete').on('click', function () {
                var filename = $(this).siblings('.file-name').text();
                if (confirm("Are you sure you want to delete this file?")) {
                    $.ajax({
                        url: '/delete/' + encodeURIComponent(filename),
                        type: 'DELETE',
                        success: function (response) {
                            alert(response.message);
                            location.reload();
                        },
                        error: function (xhr, status, error) {
                            console.error('Error:', error);
                            alert('An error occurred while deleting the file.');
                        }
                    });
                }
            });

            // Delete table
            $('.table-delete').on('click', function () {
                var tableName = $(this).closest('table').attr('id');
                if (confirm("Are you sure you want to delete this table?")) {
                    $.ajax({
                        url: '/delete_table/' + encodeURIComponent(tableName),
                        type: 'DELETE',
                        success: function (response) {
                            alert(response.message);
                            location.reload();
                        },
                        error: function (xhr, status, error) {
                            console.error('Error:', error);
                            alert('An error occurred while deleting the table.');
                        }
                    });
                }
            });

            // Run /init
            $('#run-init').on('click', function () {
                $.get('/init')
                    .done(function () {
                        console.log('Request successful');
                    })
                    .fail(function (xhr, status, error) {
                        console.error('Request failed:', error);
                    });
            });
          // push to git
          $('#push-git').on('click', function () {
                $.get('/push-git')
                    .done(function () {
                        console.log('Request successful');
                    })
                    .fail(function (xhr, status, error) {
                        console.error('Request failed:', error);
                    });
            });
            // Normalize file
            $('.file-normalize').on('click', function () {
                var filename = $(this).siblings('.file-name').text();
                $.post('/normalize', { filename: filename })
                    .done(function (response) {
                        if (response.success) {
                            alert('File normalized successfully!');
                        } else {
                            alert('File normalization failed.');
                        }
                    })
                    .fail(function (xhr, status, error) {
                        console.error('Error:', error);
                        alert('An error occurred while normalizing the file.');
                    });
            });

            // Load data
            $('#load-data').on('click', function () {
                $.get('/load')
                    .done(function () {
                        console.log('Request successful');
                        location.reload();
                    })
                    .fail(function (xhr, status, error) {
                        console.error('Request failed:', error);
                    });
            });

            // Sort table on header click
            $('th').on('click', function () {
                var column = $(this).index();
                sortTable(column);
            });

            function sortTable(column) {
                var table, rows, switching, i, x, y, shouldSwitch;
                table = document.getElementById("data-table");
                switching = true;
                while (switching) {
                    switching = false;
                    rows = table.rows;
                    for (i = 1; i < (rows.length - 1); i++) {
                        shouldSwitch = false;
                        x = rows[i].getElementsByTagName("TD")[column];
                        y = rows[i + 1].getElementsByTagName("TD")[column];
                        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                            shouldSwitch = true;
                            break;
                        }
                    }
                    if (shouldSwitch) {
                        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                        switching = true;
                    }
                }
            }
        });
    </script>
</body>

</html>
```

