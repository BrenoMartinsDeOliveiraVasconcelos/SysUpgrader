#!/bin/python3

import os
import datetime
import subprocess
import json

class PackageManagerNotFound(Exception):
    pass

# Package managers suported
PACKAGE_MANAGERS = json.load(open("config.json"))

# Get current time
def now()->str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Screen logging function
def console_log(message: str, tp: int):
    """
    Log a message to the console with a timestamp and type.

    types:
        0: INFO
        1: SUCCESS
        2: WARNING
        3: ERROR

    :param message: The message to log
    :param tp: The type of message as an integer
    """
    types = ["INFO", "SUCCESS", "WARNING", "ERROR"]
    colors = ["\033[0;37m", "\033[0;32m", "\033[0;33m", "\033[0;31m"]

    print(colors[tp], end="")
    print(f"[{now()}] [{types[tp]}] {message}")
    print("\033[0m", end="")

# Dermine is user is sudo
def is_sudo():
    return os.geteuid() == 0


# Run package manager updates
def update_packg(package_manager: dict):
    """
    Run the given package manager with its arguments.

    :param package_manager: A dictionary with the package manager path and arguments
    :raises PackageManagerNotFound: If the package manager path does not exist
    :return: The result of subprocess.run()
    """
    package_man_path = package_manager["path"]
    if os.path.exists(package_man_path):
        # Iterate in args
        for arg in package_manager["args"]:
            args = [package_man_path]
            
            # Add args to command
            args.extend(arg.split(" "))

            # Run command
            result = subprocess.run(args)

            return result
                
    else:
        raise PackageManagerNotFound(f"Package manager {package_manager['path']} not found")


def main():
    if not is_sudo():
        console_log("You must be root to run this script", 2)
        exit(1)
    else:
        console_log("Running as root. Permission granted.", 1)

    for package_manager in PACKAGE_MANAGERS:
        console_log(f"Starting upgrade process for '{package_manager}'.", 0)
        try:
            return_data = update_packg(PACKAGE_MANAGERS[package_manager])

            if return_data.returncode == 0:
                console_log(f"Successfully updated '{package_manager}'.", 1)
            else:
                console_log(f"Failed to update '{package_manager}'. Return code: {return_data.returncode} {return_data.stderr.decode('utf-8')}.", 3)
        except PackageManagerNotFound:
            console_log(f"Package manager '{package_manager}' not found. Ignoring.", 3)

if __name__ == '__main__':
    main()
