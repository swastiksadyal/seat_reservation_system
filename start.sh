echo "Starting development server"
echo "creating database...if database already exists nothing will happen"
python createDb.py
echo "starting web server..."
python main.py