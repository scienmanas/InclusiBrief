
# Exit if error is encountered (at any point of the script)
set -o errexit

# Upgrade pip and install requirements
pip install --upgrade pip
pip install -r requirements.txt