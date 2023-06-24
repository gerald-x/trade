echo "Installing Dependencies..."
pip install -r requirements.txt

echo "Making migrations..."
python3 manage.py makemigrations userDashboard
python3 manage.py makemigrations adminDashboard
python3 manage.py migrate

echo "Collecting static files..."
python3 manage.py collectstatic

echo "Starting background processes..."
python3 manage.py background_tasks

