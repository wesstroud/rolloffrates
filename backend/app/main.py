from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg
import os
import asyncio
import logging
from typing import List, Dict, Any, Optional

from .models.dumpster_data import ScrapedData, DumpsterCompany, ServiceArea, DumpsterSize, DumpsterPrice
from .scrapers.waste_management_scraper import WasteManagementScraper
from .scrapers.budget_dumpster_scraper import BudgetDumpsterScraper
from .scrapers.liberty_dumpsters_scraper import LibertyDumpstersScraper
from .utils.data_storage import DataStorage
from .utils.scheduler import ScraperScheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Dumpster SEO API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Local development
        "https://rolloffrates.com",  # Production domain
        "https://www.rolloffrates.com",  # Production domain with www
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

data_storage = DataStorage(data_dir="data")
scheduler = ScraperScheduler(data_storage)

os.makedirs("data", exist_ok=True)
os.makedirs("logs", exist_ok=True)

@app.get("/healthz")
async def healthz():
    """Health check endpoint"""
    return {"status": "ok"}

@app.post("/scrape")
async def scrape_data(background_tasks: BackgroundTasks):
    """Trigger scraping of dumpster rental websites"""
    background_tasks.add_task(run_scrapers)
    return {"message": "Scraping started in the background"}

async def run_scrapers():
    """Run all scrapers and store the data"""
    try:
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
        
        scraped_data = ScrapedData(
            companies=[DumpsterCompany(**company) for company in all_companies],
            service_areas=[ServiceArea(**area) for area in all_service_areas],
            dumpster_sizes=[DumpsterSize(**size) for size in all_dumpster_sizes],
            prices=[DumpsterPrice(**price) for price in all_prices]
        )
        
        data_storage.save_data(scraped_data)
        logger.info("All data scraped and saved successfully")
        
    except Exception as e:
        logger.error(f"Error during scraping: {str(e)}")

@app.get("/companies", response_model=List[DumpsterCompany])
async def get_companies():
    """Get all dumpster rental companies"""
    return data_storage.get_companies()

@app.get("/service-areas", response_model=List[ServiceArea])
async def get_service_areas():
    """Get all service areas"""
    return data_storage.get_service_areas()

@app.get("/dumpster-sizes", response_model=List[DumpsterSize])
async def get_dumpster_sizes():
    """Get all dumpster sizes"""
    return data_storage.get_dumpster_sizes()

@app.get("/prices", response_model=List[DumpsterPrice])
async def get_prices():
    """Get all prices"""
    return data_storage.get_prices()

@app.get("/city/{city}")
async def get_city_data(city: str, state: Optional[str] = None):
    """Get all data for a specific city"""
    city_data = data_storage.get_data_for_city(city, state)
    if not city_data:
        raise HTTPException(status_code=404, detail=f"No data found for city: {city}")
    return city_data

@app.get("/cities")
async def get_all_cities():
    """Get a list of all cities with data"""
    service_areas = data_storage.get_service_areas()
    cities = [{"city": area.city, "state": area.state} for area in service_areas]
    unique_cities = []
    seen = set()
    for city in cities:
        key = f"{city['city']}-{city['state']}"
        if key not in seen:
            seen.add(key)
            unique_cities.append(city)
    return unique_cities

@app.on_event("startup")
async def startup_event():
    """Run on startup to ensure we have some data and start scheduler"""
    data = data_storage.load_data()
    if not data.companies:
        logger.info("No data found. Running initial scrape...")
        await run_scrapers()
    
    asyncio.create_task(scheduler.start_weekly_schedule())
    logger.info("Weekly scraper schedule started")
