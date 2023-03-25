import json
import os
import subprocess
import sys

user_data_file_name = "user_data.json"
venv_dir_name = "venv"

skip_mac_setup = False
skip_mac_setup_opt = "--skip-mac-setup"
if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        if arg == skip_mac_setup_opt:
            skip_mac_setup = True
        else:
            print(f"Unrecognized option: {arg}.")
            print(
                f"""
The only option for this script is {skip_mac_setup_opt}.
Use this option if you are not using a Mac and/or do not want to connect to the messages database.
            """
            )
            sys.exit(1)

if skip_mac_setup:
    print("Skipping Mac setup steps.\n")


def print_cmd(cmd_args):
    print(f"Running command: {' '.join(cmd_args)}")


# Create virtual environment
try:
    if os.path.exists(venv_dir_name):
        print("\nVirtual environment already exists. Not creating a new one.")
    else:
        cmd_args = ["python3", "-m", "venv", "venv"]
        print_cmd(cmd_args)
        subprocess.run(cmd_args, check=True)
except subprocess.CalledProcessError:
    print("\nFailed to create virtual environment. Exiting.")
    sys.exit(1)

# Create user_data.json if not already there
if not skip_mac_setup:
    try:
        with open(user_data_file_name, "x") as user_data_file:
            print("\nUser data file does not already exist. Creating one.")
            # Create empty user data
            json.dump(
                {"contacts": {}, "chat_ids": {}, "contact_ids": {}},
                user_data_file,
                indent=4,
            )
        # Ask for name if no previous user data exists
        name = input("Type your name as you would like it to appear: ")
        while len(name) == 0:
            name = input("Looks like you didn't type your name. Type it here: ")

        # Add contact for self
        print(f"\nAdding contact for {name}")
        with open(user_data_file_name, "r") as user_data_file:
            user_data = json.load(user_data_file)
            user_data["contact_ids"][name] = [0]
        with open(user_data_file_name, "w") as user_data_file:
            json.dump(user_data, user_data_file, indent=4)
    except FileExistsError:
        print("\nUser data file already exists.")

    # Get username
    # Can't use helpers yet because setup is not complete
    print("\nDetermining username on Mac")
    cwd = os.getcwd()
    username = cwd.split("/")[2]
    print(f"USER PROFILE is {username}")
    with open(user_data_file_name, "r") as user_data_file:
        user_data = json.load(user_data_file)
        user_data["username"] = username
    with open(user_data_file_name, "w") as user_data_file:
        json.dump(user_data, user_data_file, indent=4)

# Install dependencies
try:
    print("\nInstalling python dependencies")
    cmd_args = ["venv/bin/pip", "install", "-r", "requirements.txt"]
    print_cmd(cmd_args)
    subprocess.run(cmd_args, check=True)
except subprocess.CalledProcessError:
    print("\nFailed to install python dependencies. Exiting.")
    sys.exit(1)

try:
    print("\nInstalling node.js dependencies")
    cmd_args = ["npm", "install", "--prefix", "./ui"]
    print_cmd(cmd_args)
    subprocess.run(cmd_args, check=True)
except subprocess.CalledProcessError:
    print("\nFailed to install node.js dependencies. Exiting.")
    sys.exit(1)

# Test database access
if not skip_mac_setup:
    print("\nTesting access to database")
    try:
        cmd_args = ["venv/bin/python3", "-m", "analysis", "test_db"]
        print_cmd(cmd_args)
        subprocess.run(cmd_args, check=True)
    except subprocess.CalledProcessError as e:
        print(e)
        sys.exit(1)

print("\nSet up successfully. Run ./run.sh to start the program.")
