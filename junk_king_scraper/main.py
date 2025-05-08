import asyncio
import argparse
import os
import logging
import sys
from datetime import datetime

from utils.logger import setup_logger
from utils.email_notifier import EmailNotifier
from scraper import JunkKingScraper
from data_processor import DataProcessor

async def main():
    """
    Main function to run the Junk King pricing scraper.
    """
    parser = argparse.ArgumentParser(description="Junk King Pricing Scraper")
    parser.add_argument("--input", default="data/cities.csv", help="Path to input CSV file with cities data")
    parser.add_argument("--output-dir", default="data/output", help="Directory to save output files")
    parser.add_argument("--log-dir", default="logs", help="Directory to save log files")
    parser.add_argument("--headless", action="store_true", default=True, help="Run browser in headless mode")
    parser.add_argument("--concurrency", type=int, default=5, help="Maximum number of concurrent scraping tasks")
    parser.add_argument("--delay", type=int, default=2, help="Delay between requests in seconds")
    parser.add_argument("--retry", type=int, default=3, help="Number of retry attempts for failed requests")
    parser.add_argument("--email", help="Email address to send notifications to")
    parser.add_argument("--limit", type=int, help="Limit the number of cities to scrape (for testing)")
    args = parser.parse_args()
    
    logger = setup_logger(args.log_dir)
    logger.info("Starting Junk King pricing scraper")
    
    try:
        data_processor = DataProcessor(args.output_dir)
        
        cities_data = data_processor.load_cities_data(args.input)
        
        if args.limit and args.limit > 0:
            cities_data = cities_data[:args.limit]
            logger.info(f"Limited to {args.limit} cities for testing")
        
        scraper = JunkKingScraper(
            headless=args.headless,
            retry_attempts=args.retry,
            delay_between_requests=args.delay
        )
        
        start_time = datetime.now()
        logger.info(f"Starting scraping at {start_time}")
        
        if args.concurrency > 1:
            logger.info(f"Scraping {len(cities_data)} cities with concurrency {args.concurrency}")
            results = await scraper.scrape_cities_concurrent(cities_data, args.concurrency)
        else:
            logger.info(f"Scraping {len(cities_data)} cities sequentially")
            results = await scraper.scrape_cities(cities_data)
        
        end_time = datetime.now()
        duration = end_time - start_time
        logger.info(f"Scraping completed at {end_time}")
        logger.info(f"Total duration: {duration}")
        
        df = data_processor.process_results(results)
        
        output_file = data_processor.save_results(df)
        
        stats = data_processor.generate_statistics(df)
        
        logger.info("Scraping statistics:")
        for key, value in stats.items():
            logger.info(f"{key}: {value}")
        
        if args.email:
            smtp_server = os.environ.get("SMTP_SERVER")
            smtp_port = int(os.environ.get("SMTP_PORT", 587))
            smtp_username = os.environ.get("SMTP_USERNAME")
            smtp_password = os.environ.get("SMTP_PASSWORD")
            sender_email = os.environ.get("SENDER_EMAIL")
            
            if all([smtp_server, smtp_username, smtp_password, sender_email]):
                notifier = EmailNotifier(
                    smtp_server=smtp_server,
                    smtp_port=smtp_port,
                    username=smtp_username,
                    password=smtp_password,
                    sender_email=sender_email
                )
                
                notifier.send_completion_notification(args.email, stats)
            else:
                logger.warning("Email notification requested but SMTP settings not provided")
        
        logger.info("Junk King pricing scraper completed successfully")
        
    except Exception as e:
        logger.error(f"Error running Junk King pricing scraper: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
