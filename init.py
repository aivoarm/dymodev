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
            file.write(relative_path + os.sep + '\n')
            
            for file_name in files:
                file.write(os.path.join(relative_path, file_name) + '\n')

ignored_patterns = [
    '*.pyc',
    '*.log',
    '*.db',
    '.env',
    'secret.txt',
    'database.db',
    '.gitignore'
    '*.idea',
    '*.iml',
    '*.vscode',
    '__pycache__',
    'myenv',
    'data*',
    'templates*'
]

project_directory = os.path.dirname(os.path.abspath(__file__))
output_file = 'structure.txt'

save_directory_structure(project_directory, ignored_patterns, output_file)
