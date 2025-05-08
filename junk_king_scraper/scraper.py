import asyncio
import logging
import time
from datetime import datetime
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

logger = logging.getLogger("junk_king_scraper")

class JunkKingScraper:
    """
    Scraper class for extracting pricing data from Junk King's website.
    Uses Playwright for browser automation.
    """
    def __init__(self, headless=True, timeout=30000, retry_attempts=3, delay_between_requests=2):
        """
        Initialize the scraper with configuration options.
        
        Args:
            headless (bool): Whether to run the browser in headless mode
            timeout (int): Default timeout for Playwright operations in milliseconds
            retry_attempts (int): Number of retry attempts for failed requests
            delay_between_requests (int): Delay between requests in seconds
        """
        self.headless = headless
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.delay_between_requests = delay_between_requests
        self.base_url = "https://www.junk-king.com/pricing"
    
    async def scrape_city_pricing(self, zip_code, city, state):
        """
        Scrape pricing data for a specific city.
        
        Args:
            zip_code (str): ZIP code to search
            city (str): City name for the record
            state (str): State name for the record
            
        Returns:
            dict: Dictionary containing the scraped data or error information
        """
        logger.info(f"Scraping pricing for {city}, {state} (ZIP: {zip_code})")
        
        result = {
            "zip_code": zip_code,
            "city": city,
            "state": state,
            "min_price": None,
            "full_price": None,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "pending"
        }
        
        for attempt in range(1, self.retry_attempts + 1):
            try:
                async with async_playwright() as playwright:
                    browser = await playwright.chromium.launch(headless=self.headless)
                    context = await browser.new_context(
                        viewport={"width": 1280, "height": 720},
                        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                    )
                    
                    page = await context.new_page()
                    
                    await page.goto(self.base_url, wait_until="networkidle")
                    
                    try:
                        estimator_button = await page.wait_for_selector('button:has-text("Get Free Estimate")', timeout=10000)
                        await estimator_button.click()
                    except PlaywrightTimeoutError:
                        logger.warning(f"Could not find estimator button, trying direct interaction with ZIP input")
                    
                    zip_input = await page.wait_for_selector('input[placeholder="Enter ZIP Code"]', timeout=10000)
                    
                    await zip_input.fill("")
                    await zip_input.type(zip_code, delay=100)
                    
                    submit_button = await page.wait_for_selector('button.btn-primary:has-text("Check Availability")', timeout=5000)
                    if not submit_button:
                        submit_button = await page.wait_for_selector('button[type="submit"]', timeout=5000)
                    if not submit_button:
                        submit_button = await page.wait_for_selector('button:right-of(input[placeholder="Enter ZIP Code"])', timeout=5000)
                        
                    await submit_button.click()
                    
                    try:
                        await page.wait_for_selector('text=Good news', timeout=5000)
                        
                        get_estimate_button = await page.wait_for_selector('button:has-text("Get Free Estimate")', timeout=5000)
                        await get_estimate_button.click()
                        
                        await page.wait_for_selector('text=Dumpster Rental', timeout=10000)
                        
                        min_price_element = await page.wait_for_selector('text=Minimum >> xpath=../following-sibling::*', timeout=5000)
                        min_price_text = await min_price_element.text_content()
                        min_price = min_price_text.replace('$', '').strip()
                        
                        full_price_element = await page.wait_for_selector('text=Full >> xpath=../following-sibling::*', timeout=5000)
                        full_price_text = await full_price_element.text_content()
                        full_price = full_price_text.replace('$', '').strip()
                        
                        result["min_price"] = min_price
                        result["full_price"] = full_price
                        result["status"] = "success"
                        
                        logger.info(f"Successfully scraped pricing for {city}, {state}: Min=${min_price}, Full=${full_price}")
                        
                    except PlaywrightTimeoutError:
                        logger.warning(f"No service available for {city}, {state} (ZIP: {zip_code})")
                        result["min_price"] = "N/A"
                        result["full_price"] = "N/A"
                        result["status"] = "no_service"
                    
                    await browser.close()
                    
                    break
                    
            except Exception as e:
                logger.error(f"Error scraping {city}, {state} (ZIP: {zip_code}), attempt {attempt}/{self.retry_attempts}: {str(e)}")
                
                result["status"] = "error"
                result["error_message"] = str(e)
                
                if attempt == self.retry_attempts:
                    return result
                
                wait_time = 2 ** attempt  # Exponential backoff: 2, 4, 8 seconds
                logger.info(f"Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
        
        await asyncio.sleep(self.delay_between_requests)
        
        return result
    
    async def scrape_cities(self, cities_data):
        """
        Scrape pricing data for multiple cities.
        
        Args:
            cities_data (list): List of dictionaries containing city information
            
        Returns:
            list: List of dictionaries containing the scraped data
        """
        results = []
        
        for city_data in cities_data:
            result = await self.scrape_city_pricing(
                city_data["zip"],
                city_data["city"],
                city_data["state"]
            )
            results.append(result)
        
        return results
    
    async def scrape_cities_concurrent(self, cities_data, max_concurrency=5):
        """
        Scrape pricing data for multiple cities concurrently.
        
        Args:
            cities_data (list): List of dictionaries containing city information
            max_concurrency (int): Maximum number of concurrent scraping tasks
            
        Returns:
            list: List of dictionaries containing the scraped data
        """
        results = []
        semaphore = asyncio.Semaphore(max_concurrency)
        
        async def scrape_with_semaphore(city_data):
            async with semaphore:
                return await self.scrape_city_pricing(
                    city_data["zip"],
                    city_data["city"],
                    city_data["state"]
                )
        
        tasks = [scrape_with_semaphore(city_data) for city_data in cities_data]
        
        for completed_task in asyncio.as_completed(tasks):
            result = await completed_task
            results.append(result)
        
        return results
