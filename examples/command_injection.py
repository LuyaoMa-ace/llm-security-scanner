# examples/command_injection.py
# WARNING: This file contains INTENTIONAL security vulnerabilities for testing purposes.

import os
import subprocess

def run_command(user_input):
    """Directly passes user input to the shell — dangerous!"""
    os.system(user_input)

def ping_host(hostname):
    """Concatenates user input into a shell command string."""
    subprocess.call("ping -c 1 " + hostname, shell=True)

def backup_directory(directory):
    """Uses user-supplied path in shell command."""
    cmd = f"tar -czf backup.tar.gz {directory}"
    os.system(cmd)

def list_files(path):
    """Lists files using shell — attacker can inject extra commands."""
    result = subprocess.check_output("ls " + path, shell=True)
    return result.decode()

if __name__ == "__main__":
    user_cmd = input("Enter command: ")
    run_command(user_cmd)
