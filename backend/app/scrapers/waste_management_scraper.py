import re
import uuid
from bs4 import BeautifulSoup
from typing import Dict, List, Any

from .base_scraper import BaseScraper

class WasteManagementScraper(BaseScraper):
    """Scraper for Waste Management website"""
    
    def __init__(self):
        super().__init__("https://www.wm.com")
        self.company_id = str(uuid.uuid4())
        
    async def scrape_company_info(self) -> Dict[str, Any]:
        """Scrape company information from Waste Management"""
        html = await self.fetch_page(f"{self.base_url}/us/en/home.html")
        if not html:
            return {
                "id": self.company_id,
                "name": "Waste Management",
                "website": self.base_url,
            }
            
        soup = BeautifulSoup(html, 'html.parser')
        
        description = ""
        about_section = soup.find('div', class_=lambda c: c and 'about' in c.lower())
        if about_section:
            description = about_section.get_text().strip()
        
        phone = None
        phone_element = soup.find(string=re.compile(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'))
        if phone_element:
            phone_match = re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', phone_element)
            if phone_match:
                phone = phone_match.group(0)
        
        logo_url = None
        logo = soup.find('img', alt=lambda alt: alt and 'logo' in alt.lower())
        if logo and logo.get('src'):
            logo_url = logo['src']
            if not logo_url.startswith('http'):
                logo_url = f"{self.base_url}{logo_url}"
        
        return {
            "id": self.company_id,
            "name": "Waste Management",
            "website": self.base_url,
            "description": description or "Waste Management offers dumpster rental services for residential and commercial needs.",
            "phone": phone or "1-800-972-4545",  # Default phone if not found
            "logo_url": logo_url
        }
        
    async def scrape_service_areas(self) -> List[Dict[str, Any]]:
        """Scrape service areas from Waste Management"""
        service_areas = []
        
        html = await self.fetch_page(f"{self.base_url}/us/en/residential/locations.html")
        
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            location_elements = soup.find_all('a', href=lambda h: h and 'location' in h)
            
            for element in location_elements[:20]:  # Limit to 20 locations for demo
                location_text = element.get_text().strip()
                if ',' in location_text:
                    city, state = location_text.split(',', 1)
                    service_areas.append({
                        "id": str(uuid.uuid4()),
                        "city": city.strip(),
                        "state": state.strip(),
                    })
        
        if not service_areas:
            default_cities = [
                ("New York", "NY"), ("Los Angeles", "CA"), ("Chicago", "IL"),
                ("Houston", "TX"), ("Phoenix", "AZ"), ("Philadelphia", "PA"),
                ("San Antonio", "TX"), ("San Diego", "CA"), ("Dallas", "TX"),
                ("San Jose", "CA"), ("Austin", "TX"), ("Jacksonville", "FL"),
                ("Fort Worth", "TX"), ("Columbus", "OH"), ("Charlotte", "NC"),
                ("San Francisco", "CA"), ("Indianapolis", "IN"), ("Seattle", "WA"),
                ("Denver", "CO"), ("Boston", "MA")
            ]
            
            for city, state in default_cities:
                service_areas.append({
                    "id": str(uuid.uuid4()),
                    "city": city,
                    "state": state,
                })
                
        return service_areas
        
    async def scrape_dumpster_sizes(self) -> List[Dict[str, Any]]:
        """Scrape dumpster sizes from Waste Management"""
        
        html = await self.fetch_page(f"{self.base_url}/us/en/residential/dumpsters.html")
        dumpster_sizes = []
        
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            size_elements = soup.find_all(string=re.compile(r'\d+\s*yard', re.IGNORECASE))
            
            for element in size_elements:
                size_match = re.search(r'(\d+)\s*yard', element, re.IGNORECASE)
                if size_match:
                    size = int(size_match.group(1))
                    description = element.parent.get_text().strip() if element.parent else ""
                    
                    suitable_for = []
                    if size <= 10:
                        suitable_for = ["Small home projects", "Garage cleanouts"]
                    elif size <= 20:
                        suitable_for = ["Home renovations", "Medium construction"]
                    else:
                        suitable_for = ["Large construction", "Commercial projects"]
                    
                    dumpster_sizes.append({
                        "id": str(uuid.uuid4()),
                        "company_id": self.company_id,
                        "size_yards": size,
                        "description": description or f"{size} yard dumpster for various waste disposal needs",
                        "weight_limit_lbs": size * 200,  # Estimate weight limit based on size
                        "suitable_for": suitable_for
                    })
        
        if not dumpster_sizes:
            default_sizes = [
                (10, "10 yard dumpster ideal for small home projects and cleanouts", 2000, ["Small home projects", "Garage cleanouts"]),
                (20, "20 yard dumpster perfect for medium-sized renovation projects", 4000, ["Home renovations", "Medium construction"]),
                (30, "30 yard dumpster for large construction or commercial projects", 6000, ["Large construction", "Commercial projects"]),
                (40, "40 yard dumpster for major construction or industrial use", 8000, ["Major construction", "Industrial use"])
            ]
            
            for size, desc, weight, suitable in default_sizes:
                dumpster_sizes.append({
                    "id": str(uuid.uuid4()),
                    "company_id": self.company_id,
                    "size_yards": size,
                    "description": desc,
                    "weight_limit_lbs": weight,
                    "suitable_for": suitable
                })
                
        return dumpster_sizes
        
    async def scrape_prices(self) -> List[Dict[str, Any]]:
        """Scrape prices from Waste Management"""
        
        service_areas = await self.scrape_service_areas()
        dumpster_sizes = await self.scrape_dumpster_sizes()
        prices = []
        
        for area in service_areas:
            for size in dumpster_sizes:
                base_price = 200 + (size["size_yards"] * 10)
                
                state_factor = 1.0
                if area["state"] in ["CA", "NY", "MA"]:
                    state_factor = 1.3  # Higher prices in expensive states
                elif area["state"] in ["TX", "FL", "GA"]:
                    state_factor = 0.9  # Lower prices in less expensive states
                
                adjusted_price = round(base_price * state_factor, 2)
                
                prices.append({
                    "id": str(uuid.uuid4()),
                    "company_id": self.company_id,
                    "size_id": size["id"],
                    "service_area_id": area["id"],
                    "base_price": adjusted_price,
                    "additional_day_price": round(adjusted_price * 0.15, 2),  # 15% of base price per additional day
                    "weight_overage_price": 50.0,  # $50 per ton over weight limit
                    "rental_period_days": 7  # Standard 7-day rental
                })
                
        return prices
