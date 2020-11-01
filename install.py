import json
import subprocess

procs = []

# Install dependenc
pip_install = subprocess.Popen(['pip', 'install', '-r', 'requirements.txt'])
procs.append(pip_install)
#npm_install = subprocess.Popen(['npm', 'install'])
#procs.append(npm_install)

# Create user_data.json if not already there
try:
    with open('user_data.json', 'x') as user_data_file:
        json.dump({}, user_data_file)
except FileExistsError:
    pass

# Get username
with open('user_data.json', 'r') as user_data_file:
    pwd = subprocess.Popen(['pwd'], stdout=subprocess.PIPE)
    username = subprocess.check_output(['cut', '-d/', '-f3'], stdin=pwd.stdout)
    username = username.decode('utf-8')[:-1]
    print(f'Username is {username}')
    user_data = json.load(user_data_file)
    user_data['username'] = username
with open('user_data.json', 'w') as user_data_file:
    json.dump(user_data, user_data_file, indent=4)

# Test database access
test_db = subprocess.Popen(['python3', '-m', 'analysis', 'test_db'])
procs.append(test_db)

for proc in procs:
    while proc.poll() is None:
        pass

pip_install.terminate()

print('Done setting up.')
