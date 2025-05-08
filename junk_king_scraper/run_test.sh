
source venv/bin/activate

echo "Running test with sample ZIP code..."
python test_scraper.py

echo "Running main scraper with limited cities..."
python main.py --limit 3 --log-dir logs
