# Dumpsters.com Price Scraper

This script scrapes dumpster pricing information from dumpsters.com for a list of addresses.

## Requirements

- Python 3.8+
- Chrome browser installed
- Required Python packages (install with `pip install -r requirements.txt`):
  - selenium
  - pandas
  - webdriver-manager

## Setup

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the script with:

```
python dumpsters_scraper.py
```

The script will:
1. Read addresses from the input CSV file
2. Navigate to dumpsters.com/cart for each address
3. Fill out the form with the address and select:
   - "Home/Garage Cleanout" for "What do you need the dumpster for?"
   - "Mixed Household Trash" for "What are you throwing away?"
4. Extract pricing data for each available dumpster size (10, 15, 20, 30 yard)
5. Save the results to `dumpster_prices.csv`

## Output Format

The output CSV file contains the following columns:
- `address`: The address used for the search
- `dumpster_size`: The size of the dumpster (e.g., "10 Yard")
- `price`: The price of the dumpster

## Notes

- The script uses a headless Chrome browser, so you won't see the browser window during execution
- A small delay (2 seconds) is added between requests to avoid overloading the server
- If the script encounters an error with an address, it will log the error and continue with the next address
