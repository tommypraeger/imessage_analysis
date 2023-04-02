import os
import subprocess
import sys
import venv


def print_cmd(cmd_args):
    print(f"Running command: {' '.join(cmd_args)}")


# Create virtual environment before import local files
venv_dir_name = "venv"
if os.path.exists(venv_dir_name):
    print("\nVirtual environment already exists. Not creating a new one.")
else:
    venv.create(venv_dir_name, with_pip=True)

# Install python dependencies
try:
    print("\nInstalling python dependencies")
    cmd_args = [f"{venv_dir_name}/bin/pip", "install", "-r", "requirements.txt"]
    print_cmd(cmd_args)
    subprocess.run(cmd_args, check=True)
except subprocess.CalledProcessError:
    print("\nFailed to install python dependencies. Exiting.")
    sys.exit(1)

# Add venv to PYTHONPATH if not already activated
if sys.prefix == sys.base_prefix:
    found_site_packages = False
    for root, dirs, files in os.walk(f"{venv_dir_name}/lib"):
        for dir in dirs:
            if dir.startswith("python"):
                site_packages_dir = f"{venv_dir_name}/lib/{dir}/site-packages"
                if os.path.exists(site_packages_dir):
                    sys.path.append(site_packages_dir)
                    found_site_packages = True
    if not found_site_packages:
        print(
            "\nFailed to use packages in virtual environment. "
            "Try activating the virtual environment using `source venv/bin/activate` and run the script again."
        )
        sys.exit(1)
else:
    print("\nVirtual environment already activated.")


from src.utils.constants import USER_DATE_FILE_NAME
from src.utils.helpers import load_user_data, save_user_data
from src.utils.sql import test_db

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


# Create user_data.json if not already there
if not skip_mac_setup:
    if os.path.isfile(USER_DATE_FILE_NAME):
        print("\nUser data file already exists.")
    else:
        print("\nUser data file does not already exist. Creating one.")
        save_user_data({"contacts": {}, "chat_ids": {}, "contact_ids": {}})

        # Ask for name if no previous user data exists
        name = input("Type your name as you would like it to appear: ")
        while len(name) == 0:
            name = input("Looks like you didn't type your name. Type it here: ")

        # Add contact for self
        print(f"\nAdding contact for {name}")
        user_data = load_user_data()
        user_data["contact_ids"][name] = [0]
        save_user_data(user_data)

    # Get username
    # Can't use helpers yet because setup is not complete
    print("\nDetermining username on Mac")
    cwd = os.getcwd()
    username = cwd.split("/")[2]
    print(f"USER PROFILE is {username}")
    user_data = load_user_data()
    user_data["username"] = username
    save_user_data(user_data)

# Install node modules
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
    status_code, msg = test_db()
    print(msg)
    if status_code != 0:
        sys.exit(status_code)

print("\nSet up successfully. Run ./run.sh to start the program.")
