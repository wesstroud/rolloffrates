import asyncio
import logging
from scraper import JunkKingScraper
from utils.logger import setup_logger

async def test_sample_zip():
    """
    Test the scraper with a sample ZIP code to verify functionality.
    """
    logger = setup_logger()
    logger.setLevel(logging.INFO)
    
    sample_data = {
        "zip": "90071",
        "city": "Los Angeles",
        "state": "California"
    }
    
    scraper = JunkKingScraper(headless=True, retry_attempts=2)
    
    logger.info(f"Testing scraper with ZIP code: {sample_data['zip']}")
    result = await scraper.scrape_city_pricing(
        sample_data["zip"],
        sample_data["city"],
        sample_data["state"]
    )
    
    logger.info("Scraping result:")
    for key, value in result.items():
        logger.info(f"{key}: {value}")
    
    return result

if __name__ == "__main__":
    asyncio.run(test_sample_zip())
