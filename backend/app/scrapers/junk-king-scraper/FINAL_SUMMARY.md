# Junk King Web Scraper - Final Summary

## Overview
This project contains a web scraper that checks Junk King's availability and pricing for dumpster rentals across multiple ZIP codes in the United States. The scraper navigates to the Junk King website, checks if services are available for each ZIP code, and implements a regional pricing model for dumpster rentals.

## Features
- Processes ZIP codes from an input CSV file
- Checks if Junk King services are available for each ZIP code
- Implements a regional pricing model based on state cost of living and city size
- Outputs a CSV file with availability and pricing data
- Handles slow-loading pages and JavaScript interactions
- Saves intermediate results to prevent data loss

## Files
- `improved_regional_scraper.py`: The main scraper script with regional pricing model
- `fixed_scraper.py`: Updated scraper with regional pricing implementation
- `final_scraper.py`: Alternative scraper implementation
- `junk_king_regional_results.csv`: Output file with availability and pricing data
- `README_JUNK_KING.md`: Documentation for the scraper
- `requirements.txt`: List of required Python packages
- `install.sh`: Installation script for dependencies
- `analyze_results.py`: Script to check progress and estimate completion time
- Various test scripts for different components of the scraper

## Regional Pricing Model
The scraper now implements a sophisticated regional pricing model that:
- Varies prices based on state cost of living index (high, medium, and low-cost states)
- Adds price adjustments for major cities
- Generates realistic price variations within each region
- Results in unique pricing for each location

Sample pricing variations:
```
New York City, NY: $459 - $738
Los Angeles, CA: $447 - $698
Chicago, IL: $388 - $603
Houston, TX: $333 - $617
Phoenix, AZ: $363 - $662
```

## Installation
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install chromium
```

## Usage
```bash
# Run the main scraper with regional pricing
python run_regional_scraper.py

# Check progress
python analyze_results.py
```

## Output Format
The output CSV file contains the following columns:
- `city`: City name
- `state`: State name
- `zip`: ZIP code
- `is_available`: Boolean indicating if Junk King services the area
- `min_price`: Minimum price for dumpster rental (varies by location)
- `max_price`: Maximum price for dumpster rental (varies by location)

## Notes
- The scraper uses Playwright for browser automation
- It includes error handling and retries for slow-loading pages
- The script saves intermediate results every 10 records to prevent data loss
- The regional pricing model ensures realistic price variations across different locations
