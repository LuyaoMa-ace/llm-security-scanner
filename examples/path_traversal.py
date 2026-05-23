# examples/path_traversal.py
# WARNING: This file contains INTENTIONAL security vulnerabilities for testing purposes.

import os

def read_user_file(filename):
    """No path validation — user can read any file on the system."""
    with open(filename, 'r') as f:
        return f.read()

def save_report(output_path, content):
    """Writes to any path the user specifies — can overwrite system files."""
    with open(output_path, 'w') as f:
        f.write(content)

def get_config(config_name):
    """Attempts to restrict path but still vulnerable to directory traversal."""
    config_dir = "/app/configs/"
    path = config_dir + config_name  # attacker uses ../../etc/passwd
    with open(path, 'r') as f:
        return f.read()

def serve_static(base_dir, filename):
    """Joins paths without sanitization."""
    full_path = os.path.join(base_dir, filename)
    with open(full_path, 'rb') as f:
        return f.read()

if __name__ == "__main__":
    fname = input("Enter file to read: ")
    print(read_user_file(fname))
