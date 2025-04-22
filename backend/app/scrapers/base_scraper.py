import aiohttp
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, List, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """Base class for all scrapers"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            
    async def fetch_page(self, url: str) -> str:
        """Fetch a page and return its HTML content"""
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    logger.error(f"Failed to fetch {url}: Status {response.status}")
                    return ""
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return ""
            
    @abstractmethod
    async def scrape_company_info(self) -> Dict[str, Any]:
        """Scrape company information"""
        pass
        
    @abstractmethod
    async def scrape_service_areas(self) -> List[Dict[str, Any]]:
        """Scrape service areas"""
        pass
        
    @abstractmethod
    async def scrape_dumpster_sizes(self) -> List[Dict[str, Any]]:
        """Scrape dumpster sizes"""
        pass
        
    @abstractmethod
    async def scrape_prices(self) -> List[Dict[str, Any]]:
        """Scrape prices"""
        pass
        
    async def scrape_all(self) -> Dict[str, Any]:
        """Scrape all data"""
        company_info = await self.scrape_company_info()
        service_areas = await self.scrape_service_areas()
        dumpster_sizes = await self.scrape_dumpster_sizes()
        prices = await self.scrape_prices()
        
        return {
            "company": company_info,
            "service_areas": service_areas,
            "dumpster_sizes": dumpster_sizes,
            "prices": prices
        }
