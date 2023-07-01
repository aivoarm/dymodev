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
