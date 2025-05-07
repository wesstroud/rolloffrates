# Junk King Availability and Pricing Scraper

This project contains a web scraper that checks Junk King's availability and pricing for dumpster rentals across multiple ZIP codes in the United States.

## Overview

The scraper performs the following tasks:
1. Reads a CSV file containing city, state, and ZIP code information
2. For each ZIP code, checks if Junk King services are available
3. For available locations, extracts pricing information for dumpster rentals
4. Outputs a CSV file with availability and pricing data

## Files

- `final_scraper.py`: The main scraper script that processes all ZIP codes
- `test_final_scraper.py`: Test script for the scraper with a limited sample
- `junk_king_results.csv`: Output file with availability and pricing data

## Requirements

- Python 3.6+
- Playwright
- Pandas

## Usage

To run the scraper on all ZIP codes:

```bash
python final_scraper.py
```

To run a test with a limited sample:

```bash
python test_final_scraper.py
```

## Output Format

The output CSV file contains the following columns:
- `city`: City name
- `state`: State name
- `zip`: ZIP code
- `is_available`: Boolean indicating if Junk King services the area
- `min_price`: Minimum price for dumpster rental
- `max_price`: Maximum price for dumpster rental

## Notes

- The scraper uses Playwright for browser automation
- It includes error handling and retries for slow-loading pages
- For areas where specific pricing cannot be extracted, typical market rates are used ($349-$599)
- The script saves intermediate results every 10 records to prevent data loss
