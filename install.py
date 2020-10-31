import subprocess

pip_install = subprocess.Popen(['pip', 'install', '-r', 'requirements.txt'])
npm_install = subprocess.Popen(['npm', 'install'])

# Get USERNAME

# Test database access

while pip_install.poll() is None or npm_install.poll() is None:
    pass

print('Done setting up.')
