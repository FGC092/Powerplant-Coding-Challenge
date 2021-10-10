# Create virtual environment
echo 'Creating virtual environment (env)...'
python3 -m venv venv

# Activate virtual environment
echo 'Activating virtual environment (env)...'
source venv/bin/activate

# Install project requirements
echo 'Installing project requirements...'
pip install -r requirements.txt

# Launch project demo server in port 8888
echo 'Starting server...'
python3 manage.py runserver 8888