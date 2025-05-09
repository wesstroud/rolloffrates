"""
Dumpsters.com Price Scraper - Command Line Interface
This script provides a command-line interface to run the dumpster scraper
with various options.
"""

import os
import argparse
import asyncio
from final_headless_scraper import main as scraper_main

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Scrape dumpster prices from dumpsters.com')
    
    parser.add_argument(
        '--input', '-i',
        type=str,
        help='Path to input CSV file with addresses'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='dumpster_prices.csv',
        help='Path to output CSV file (default: dumpster_prices.csv)'
    )
    
    parser.add_argument(
        '--limit', '-l',
        type=int,
        default=0,
        help='Limit the number of addresses to process (default: process all)'
    )
    
    parser.add_argument(
        '--debug', '-d',
        action='store_true',
        help='Enable debug mode with additional logging and screenshots'
    )
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    
    if args.input:
        os.environ['DUMPSTER_INPUT_FILE'] = args.input
    
    if args.output:
        os.environ['DUMPSTER_OUTPUT_FILE'] = args.output
    
    if args.limit:
        os.environ['DUMPSTER_LIMIT'] = str(args.limit)
    
    if args.debug:
        os.environ['DUMPSTER_DEBUG'] = '1'
    
    asyncio.run(scraper_main())
