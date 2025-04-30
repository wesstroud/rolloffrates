import asyncio
import logging
from datetime import datetime, timedelta
import os
from pathlib import Path

from ..scrapers.waste_management_scraper import WasteManagementScraper
from ..scrapers.budget_dumpster_scraper import BudgetDumpsterScraper
from ..scrapers.liberty_dumpsters_scraper import LibertyDumpstersScraper
from ..utils.data_storage import DataStorage

logger = logging.getLogger(__name__)

log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

file_handler = logging.FileHandler(log_dir / "scraper_runs.log")
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class ScraperScheduler:
    """Scheduler for running scrapers on a regular basis"""
    
    def __init__(self, data_storage: DataStorage):
        self.data_storage = data_storage
        self.running = False
        self.last_run = None
    
    async def run_scrapers(self):
        """Run all scrapers and store the data"""
        try:
            logger.info("Starting scheduled scraper run")
            
            scrapers = [
                WasteManagementScraper(),
                BudgetDumpsterScraper(),
                LibertyDumpstersScraper()
            ]
            
            all_companies = []
            all_service_areas = []
            all_dumpster_sizes = []
            all_prices = []
            
            for scraper in scrapers:
                try:
                    async with scraper:
                        logger.info(f"Starting scraper for {scraper.__class__.__name__}")
                        
                        company = await scraper.scrape_company_info()
                        all_companies.append(company)
                        
                        service_areas = await scraper.scrape_service_areas()
                        all_service_areas.extend(service_areas)
                        
                        dumpster_sizes = await scraper.scrape_dumpster_sizes()
                        all_dumpster_sizes.extend(dumpster_sizes)
                        
                        prices = await scraper.scrape_prices()
                        all_prices.extend(prices)
                        
                        logger.info(f"Completed scraper for {scraper.__class__.__name__}")
                except Exception as e:
                    logger.error(f"Error in {scraper.__class__.__name__} scraper: {str(e)}")
            
            from ..models.dumpster_data import ScrapedData, DumpsterCompany, ServiceArea, DumpsterSize, DumpsterPrice
            
            scraped_data = ScrapedData(
                companies=[DumpsterCompany(**company) for company in all_companies],
                service_areas=[ServiceArea(**area) for area in all_service_areas],
                dumpster_sizes=[DumpsterSize(**size) for size in all_dumpster_sizes],
                prices=[DumpsterPrice(**price) for price in all_prices]
            )
            
            self.data_storage.save_data(scraped_data)
            self.last_run = datetime.now()
            logger.info(f"Scheduled scraper run completed successfully at {self.last_run}")
            
        except Exception as e:
            logger.error(f"Error during scheduled scraping: {str(e)}")
    
    async def start_weekly_schedule(self):
        """Start the weekly scraper schedule"""
        self.running = True
        logger.info("Starting weekly scraper schedule")
        
        while self.running:
            await self.run_scrapers()
            
            now = datetime.now()
            next_run = now + timedelta(days=7)
            seconds_until_next_run = (next_run - now).total_seconds()
            
            logger.info(f"Next scraper run scheduled for {next_run}")
            
            await asyncio.sleep(seconds_until_next_run)
    
    def stop_schedule(self):
        """Stop the weekly scraper schedule"""
        self.running = False
        logger.info("Weekly scraper schedule stopped")
