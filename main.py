from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os
import subprocess
import sqlite3

app = Flask(__name__)
app.secret_key = 'asdasdsd9127312b9sy1s1021102¡'  # Set a secret key for session management
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    # Load and return the User object based on the user_id
    from models import User
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
#@login_required
def index():
    # Check if the database file exists
    if not os.path.exists('database.db'):
        return render_template('index.html', data_list=["a"], filenames=["b"])

    # Connect to the SQLite database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Retrieve data from the database
    cursor.execute('SELECT data FROM normalized_data')
    rows = cursor.fetchall()
    data_list = [row[0] for row in rows] if rows else []

    # Close the connection
    conn.close()

    if not data_list:
        return render_template('index.html', data_list=["a"], filenames=["b"])

    # Get a list of file names in the "data" folder
    data_folder = os.path.join(app.root_path, 'data')
    filenames = [filename for filename in os.listdir(data_folder) if os.path.isfile(os.path.join(data_folder, filename))]

    # Pass the data to the template
    return render_template('index.html', data_list=data_list, filenames=filenames)

@app.route('/upload', methods=['POST'])
def upload_data():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    folder_path = 'data'  # Path to the "data" folder
    file_path = os.path.join(folder_path, filename)

    # Create the "data" folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

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
    for current_filename in filenames:
        # Perform the normalization logic here using the current_filename

        # Example normalization code (replace with your actual implementation)
        normalized_data = normalize_data(current_filename, file_format="csv")

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
    normalized_filename = "n_" + filename
    return normalized_filename

if __name__ == '__main__':
    app.run(debug=True)
