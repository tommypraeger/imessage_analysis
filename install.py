import json
import subprocess

user_data_file_name = './ui/public/user_data.json'

# Ask for name in beginning
name = input('Type your name as you would like it to appear: ')
while len(name) == 0:
    name = input('Looks like you didn\'t type your name. Type it here: ')


# Install dependencies
pip_install = subprocess.Popen(['pip', 'install', '-r', 'requirements.txt'])
npm_install = subprocess.Popen(['npm', 'install', '--prefix', './ui'])
install_procs = [pip_install, npm_install]

# Create user_data.json if not already there
try:
    with open(user_data_file_name, 'x') as user_data_file:
        json.dump({
            'contacts': {},
            'chat_ids': {},
            'contact_ids': {}
        }, user_data_file, indent=4)
except FileExistsError:
    pass

# Get username
# Can't use helpers yet because setup is not complete
pwd = subprocess.Popen(['pwd'], stdout=subprocess.PIPE)
username = subprocess.check_output(['cut', '-d/', '-f3'], stdin=pwd.stdout)
username = username.decode('utf-8')[:-1]
print(f'USER PROFILE is {username}')
with open(user_data_file_name, 'r') as user_data_file:
    user_data = json.load(user_data_file)
    user_data['username'] = username
with open(user_data_file_name, 'w') as user_data_file:
    json.dump(user_data, user_data_file, indent=4)

for proc in install_procs:
    while proc.poll() is None:
        pass

for proc in install_procs:
    proc.terminate()

# Test database access
test_db = subprocess.Popen(['python3', '-m', 'analysis', 'test_db'])
while test_db.poll() is None:
    pass
test_db.terminate()

# Add contact for self
with open(user_data_file_name, 'r') as user_data_file:
    user_data = json.load(user_data_file)
    user_data['contact_ids'][name] = [0]
with open(user_data_file_name, 'w') as user_data_file:
    json.dump(user_data, user_data_file, indent=4)

print('Done setting up.')
