echo "Installing Dependencies..."
pip3 install -r requirements.txt

echo "Installing pm2..."
npm install -g pm2

echo "Making migrations..."
python3 manage.py makemigrations background_task
python3 manage.py migrate background_task
python3 manage.py makemigrations userDashboard
python3 manage.py makemigrations adminDashboard
python3 manage.py migrate

echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "Starting background task process..."
pm2 start python3 manage.py process_tasks --name background_tasks

