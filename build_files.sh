echo "Installing Dependencies..."
pip3.8 -m pip install -r requirements.txt

echo "Making migrations..."
python3.8 manage.py makemigrations userDashboard
python3.8 manage.py makemigrations adminDashboard
python3.8 manage.py migrate

echo "Collecting static files..."
python3.8 manage.py collectstatic

echo "Starting background processes..."
python3.8 manage.py background_tasks

