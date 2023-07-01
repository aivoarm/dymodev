import subprocess

command = """
    cd dymodev
    venv -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
"""

subprocess.run(command, shell=True, executable="/bin/bash", check=True)
