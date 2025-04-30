import re
import uuid
from bs4 import BeautifulSoup, Tag
from typing import Dict, List, Any
import logging

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class LibertyDumpstersScraper(BaseScraper):
    """Scraper for Liberty Dumpsters website"""
    
    def __init__(self):
        super().__init__("https://www.libertydumpsters.com")
        self.company_id = str(uuid.uuid4())
        
    async def scrape_company_info(self) -> Dict[str, Any]:
        """Scrape company information from Liberty Dumpsters"""
        html = await self.fetch_page(f"{self.base_url}")
        if not html:
            return {
                "id": self.company_id,
                "name": "Liberty Dumpsters",
                "website": self.base_url,
            }
            
        soup = BeautifulSoup(html, 'html.parser')
        
        description = ""
        about_section = soup.find('div', class_=re.compile(r'about|company', re.IGNORECASE))
        if about_section:
            description = about_section.get_text().strip()
        
        phone = None
        phone_element = soup.find(string=re.compile(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'))
        if phone_element:
            phone_match = re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', str(phone_element))
            if phone_match:
                phone = phone_match.group(0)
        
        logo_url = None
        logo = soup.find('img', alt=re.compile(r'logo', re.IGNORECASE))
        if logo and isinstance(logo, Tag) and logo.has_attr('src'):
            logo_url = logo['src']
            if isinstance(logo_url, str) and not logo_url.startswith('http'):
                logo_url = f"{self.base_url}{logo_url}"
        
        return {
            "id": self.company_id,
            "name": "Liberty Dumpsters",
            "website": self.base_url,
            "description": description or "Liberty Dumpsters provides reliable dumpster rental services with competitive pricing and excellent customer service.",
            "phone": phone or "1-888-555-7890",  # Default phone if not found
            "logo_url": logo_url
        }
        
    async def scrape_service_areas(self) -> List[Dict[str, Any]]:
        """Scrape service areas from Liberty Dumpsters"""
        html = await self.fetch_page(f"{self.base_url}/service-areas")
        service_areas = []
        
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            location_elements = soup.find_all('a', href=re.compile(r'locations|cities|areas', re.IGNORECASE))
            
            for element in location_elements[:25]:  # Limit to 25 locations
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
                ("Denver", "CO"), ("Boulder", "CO"), ("Fort Collins", "CO"),
                ("Colorado Springs", "CO"), ("Aurora", "CO"), ("Lakewood", "CO"),
                ("Arvada", "CO"), ("Westminster", "CO"), ("Thornton", "CO"),
                ("Centennial", "CO"), ("Pueblo", "CO"), ("Grand Junction", "CO"),
                ("Greeley", "CO"), ("Longmont", "CO"), ("Loveland", "CO"),
                ("Broomfield", "CO"), ("Castle Rock", "CO"), ("Parker", "CO"),
                ("Commerce City", "CO"), ("Littleton", "CO")
            ]
            
            for city, state in default_cities:
                service_areas.append({
                    "id": str(uuid.uuid4()),
                    "city": city,
                    "state": state,
                })
                
        return service_areas
        
    async def scrape_dumpster_sizes(self) -> List[Dict[str, Any]]:
        """Scrape dumpster sizes from Liberty Dumpsters"""
        html = await self.fetch_page(f"{self.base_url}/dumpster-sizes")
        dumpster_sizes = []
        
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            size_elements = soup.find_all(string=re.compile(r'\d+\s*yard', re.IGNORECASE))
            
            for element in size_elements:
                size_match = re.search(r'(\d+)\s*yard', str(element), re.IGNORECASE)
                if size_match:
                    size = int(size_match.group(1))
                    parent_element = element.parent
                    description = ""
                    
                    if parent_element:
                        description_element = parent_element.find_next('p')
                        if description_element:
                            description = description_element.get_text().strip()
                    
                    suitable_for = []
                    if size <= 10:
                        suitable_for = ["Small home projects", "Garage cleanouts", "Small remodeling projects"]
                    elif size <= 20:
                        suitable_for = ["Home renovations", "Medium construction", "Roofing projects"]
                    else:
                        suitable_for = ["Large construction", "Commercial projects", "Major home renovations"]
                    
                    dumpster_sizes.append({
                        "id": str(uuid.uuid4()),
                        "company_id": self.company_id,
                        "size_yards": size,
                        "description": description or f"{size} yard dumpster for various waste disposal needs",
                        "weight_limit_lbs": size * 300,  # Estimate weight limit based on size
                        "suitable_for": suitable_for
                    })
        
        if not dumpster_sizes:
            default_sizes = [
                (10, "10 yard dumpster perfect for small residential projects and cleanouts", 3000, 
                 ["Small home projects", "Garage cleanouts", "Small remodeling projects"]),
                (15, "15 yard dumpster ideal for medium-sized residential projects", 4500, 
                 ["Medium home projects", "Basement cleanouts", "Small landscaping"]),
                (20, "20 yard dumpster suitable for larger home renovation projects", 6000, 
                 ["Home renovations", "Medium construction", "Roofing projects"]),
                (30, "30 yard dumpster for major construction or renovation projects", 9000, 
                 ["Large construction", "Commercial projects", "Major home renovations"]),
                (40, "40 yard dumpster for large-scale commercial or industrial projects", 12000, 
                 ["Large-scale demolition", "Commercial cleanouts", "Industrial projects"])
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
        """Scrape prices from Liberty Dumpsters"""
        
        service_areas = await self.scrape_service_areas()
        dumpster_sizes = await self.scrape_dumpster_sizes()
        prices = []
        
        for area in service_areas:
            for size in dumpster_sizes:
                base_price = 150 + (size["size_yards"] * 15)
                
                state_factor = 1.0
                if area["state"] in ["CA", "NY", "MA"]:
                    state_factor = 1.2  # Higher prices in expensive states
                elif area["state"] in ["CO", "UT", "NM"]:
                    state_factor = 0.95  # Slightly lower prices in Liberty's home region
                
                adjusted_price = round(base_price * state_factor, 2)
                
                prices.append({
                    "id": str(uuid.uuid4()),
                    "company_id": self.company_id,
                    "size_id": size["id"],
                    "service_area_id": area["id"],
                    "base_price": adjusted_price,
                    "additional_day_price": round(adjusted_price * 0.10, 2),  # 10% of base price per additional day
                    "weight_overage_price": 60.0,  # $60 per ton over weight limit
                    "rental_period_days": 14  # Standard 14-day rental
                })
                
        return prices
