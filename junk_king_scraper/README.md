# Junk King Pricing Scraper

This project automatically scrapes dumpster rental pricing data from Junk King's website for 351 specified cities on a monthly basis.

## Features

- Extracts minimum and full load prices for MINI dumpster rentals
- Handles 351 cities across the US
- Robust error handling and retry mechanisms
- Data validation and processing
- Automated monthly execution via GitHub Actions
- Email notifications for completion and errors
- Detailed logging

## Project Structure

```
junk_king_scraper/
├── main.py                 # Entry point script
├── scraper.py              # Core scraping logic
├── data_processor.py       # Data cleaning and validation
├── utils/
│   ├── logger.py           # Logging configuration
│   └── email_notifier.py   # Error notification
├── data/
│   ├── cities.csv          # Input data with 351 cities
│   └── output/             # Directory for monthly results
└── .github/
    └── workflows/
        └── monthly_scrape.yml  # GitHub Actions workflow
```

## Requirements

- Python 3.10+
- Playwright
- Pandas
- AsyncIO

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Install Playwright browsers:
   ```
   playwright install chromium
   ```

## Usage

### Basic Usage

```
python main.py
```

### Command Line Options

- `--input`: Path to input CSV file with cities data (default: `data/cities.csv`)
- `--output-dir`: Directory to save output files (default: `data/output`)
- `--log-dir`: Directory to save log files (default: `logs`)
- `--headless`: Run browser in headless mode (default: `True`)
- `--concurrency`: Maximum number of concurrent scraping tasks (default: `5`)
- `--delay`: Delay between requests in seconds (default: `2`)
- `--retry`: Number of retry attempts for failed requests (default: `3`)
- `--email`: Email address to send notifications to
- `--limit`: Limit the number of cities to scrape (for testing)

### Examples

Run with default settings:
```
python main.py
```

Run with custom settings:
```
python main.py --concurrency 10 --delay 1 --retry 5 --email admin@example.com
```

Test with a limited number of cities:
```
python main.py --limit 10
```

## Automated Execution

The scraper is configured to run automatically on the 1st of each month using GitHub Actions. The workflow configuration is in `.github/workflows/monthly_scrape.yml`.

## Output Format

The scraper generates a CSV file with the following columns:

- `zip_code`: ZIP code of the city
- `city`: City name
- `state`: State name
- `min_price`: Minimum price for MINI dumpster rental
- `full_price`: Full price for MINI dumpster rental
- `timestamp`: Timestamp of when the data was scraped
- `status`: Status of the scraping (success, no_service, error, validation_error)

## Email Notifications

To enable email notifications, set the following environment variables:

- `SMTP_SERVER`: SMTP server address
- `SMTP_PORT`: SMTP server port (default: 587)
- `SMTP_USERNAME`: SMTP username
- `SMTP_PASSWORD`: SMTP password
- `SENDER_EMAIL`: Sender email address
- `NOTIFICATION_EMAIL`: Email address to send notifications to

## License

This project is licensed under the MIT License - see the LICENSE file for details.
