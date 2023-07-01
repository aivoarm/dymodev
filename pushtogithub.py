import subprocess

# Run 'git add .' command
subprocess.run(['git', 'add', '.'])

# Run 'git commit -m "update"' command
subprocess.run(['git', 'commit', '-m', 'update'])

# Run 'git push remote main' command
subprocess.run(['git', 'push', 'origin', 'main'])
