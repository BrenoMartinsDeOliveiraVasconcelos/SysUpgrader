#!/usr/bin/env python3

import os
import datetime
import subprocess
import json
import shlex

class PackageManagerNotFound(Exception):
    pass

class PackageManagerIsNotExecutable(Exception):
    pass

# Package managers suported
try:
    PACKAGE_MANAGERS = json.load(open("/etc/sysupgrader/config.json"))
except FileNotFoundError:
    print("Run install.sh to install sysupgrader and generate default config.")
    exit(1)

log_path = "/var/log/sut.log"

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
        4: OUTPUT

    :param message: The message to log
    :param tp: The type of message as an integer
    """
    types = ["INFO", "SUCCESS", "WARNING", "ERROR", "OUTPUT"]
    colors = ["\033[0;37m", "\033[0;32m", "\033[0;33m", "\033[0;31m", "\033[0;37m"]
    msg = f"[{now()}] [{types[tp]}] {message}"
    
    if tp != 4:
        print(colors[tp], end="")
        print(msg)
        print("\033[0m", end="")
    else:
        print(message)

    with open(log_path, "a") as f:
        f.write(f"{msg}\n")

# Dermine is user is sudo
def is_sudo():
    return os.geteuid() == 0


# Run package manager updates

def update_packg(package_manager: dict):
    package_man_path = package_manager["path"]
    if os.path.exists(package_man_path):
        if not os.access(package_man_path, os.X_OK):
            raise PackageManagerIsNotExecutable(f"Package manager {package_manager['path']} is not executable")

        results = []
        args = []
        for command in package_manager["commands"]:
            args = [package_man_path]
            args.extend(shlex.split(command))

            proc = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            stdout_lines = []
            for line in iter(proc.stdout.readline, ''):
                stripped_line = line.rstrip('\n')
                console_log(stripped_line, 4)
                stdout_lines.append(stripped_line)
            proc.stdout.close()
            
            return_code = proc.wait()

            result = subprocess.CompletedProcess(
                args,
                return_code,
                stdout='\n'.join(stdout_lines),
                stderr=''
            )

            results.append(result)

            if return_code != 0:
                break

        return [results[-1] if results else None, " ".join(args)]
    else:
        raise PackageManagerNotFound(f"Package manager {package_manager['path']} not found")


def main():
    console_log("Started System Upgrade Tool.", 0)

    if not is_sudo():
        console_log("You must be root to run this script", 3)
        exit(1)
    else:
        console_log("Running as root. Permission granted.", 1)

    # Create log file
    if not os.path.exists(log_path):
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        open(log_path, "w+").close()

    # Error count
    errors = 0
    for package_manager in PACKAGE_MANAGERS:
        errors += 1
        console_log(f"Starting upgrade process for '{package_manager}'.", 0)
        try:
            output = update_packg(PACKAGE_MANAGERS[package_manager])
            return_data = output[0]
            command = output[1]

            if return_data.returncode == 0:
                console_log(f"Successfully updated '{package_manager}'.", 1)
                errors -= 1
            else:
                console_log(f"Failed to update '{package_manager}'. Return code: {return_data.returncode}. Command: {command}. Run it manually for more details.", 3)
        except PackageManagerNotFound:
            console_log(f"Package manager '{package_manager}' not found. Ignoring.", 3)
        except PackageManagerIsNotExecutable:
            console_log(f"Package manager path for '{package_manager}' is not executable. Ignoring.", 3)

    # Return 1 if there are errors
    if errors > 0:
        console_log(f"Execution terminated with {errors} errors. Verify {log_path} for details.", 3)
        exit(1)

if __name__ == '__main__':
    main()
