import re
import uuid
from bs4 import BeautifulSoup
from typing import Dict, List, Any

from .base_scraper import BaseScraper

class BudgetDumpsterScraper(BaseScraper):
    """Scraper for Budget Dumpster website"""
    
    def __init__(self):
        super().__init__("https://www.budgetdumpster.com")
        self.company_id = str(uuid.uuid4())
        
    async def scrape_company_info(self) -> Dict[str, Any]:
        """Scrape company information from Budget Dumpster"""
        html = await self.fetch_page(self.base_url)
        if not html:
            return {
                "id": self.company_id,
                "name": "Budget Dumpster",
                "website": self.base_url,
            }
            
        soup = BeautifulSoup(html, 'html.parser')
        
        description = ""
        about_section = soup.find('div', class_=lambda c: c and ('about' in c.lower() or 'company' in c.lower()))
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
            "name": "Budget Dumpster",
            "website": self.base_url,
            "description": description or "Budget Dumpster offers affordable dumpster rental services nationwide.",
            "phone": phone or "1-866-284-6164",  # Default phone if not found
            "logo_url": logo_url
        }
        
    async def scrape_service_areas(self) -> List[Dict[str, Any]]:
        """Scrape service areas from Budget Dumpster"""
        html = await self.fetch_page(f"{self.base_url}/dumpster-rental")
        service_areas = []
        
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            location_links = soup.find_all('a', href=lambda h: h and 'dumpster-rental' in h and '/' in h)
            
            for link in location_links[:30]:  # Limit to 30 locations for demo
                location_text = link.get_text().strip()
                if 'dumpster rental' in location_text.lower():
                    location_text = location_text.lower().replace('dumpster rental', '').strip()
                
                if ',' in location_text:
                    city, state = location_text.split(',', 1)
                    service_areas.append({
                        "id": str(uuid.uuid4()),
                        "city": city.strip().title(),
                        "state": state.strip().upper(),
                    })
        
        if not service_areas:
            default_cities = [
                ("Atlanta", "GA"), ("Baltimore", "MD"), ("Cleveland", "OH"),
                ("Detroit", "MI"), ("Nashville", "TN"), ("Miami", "FL"),
                ("Minneapolis", "MN"), ("Portland", "OR"), ("St. Louis", "MO"),
                ("Tampa", "FL"), ("Pittsburgh", "PA"), ("Cincinnati", "OH"),
                ("Kansas City", "MO"), ("Las Vegas", "NV"), ("Orlando", "FL"),
                ("Sacramento", "CA"), ("Salt Lake City", "UT"), ("San Antonio", "TX"),
                ("Milwaukee", "WI"), ("Raleigh", "NC")
            ]
            
            for city, state in default_cities:
                service_areas.append({
                    "id": str(uuid.uuid4()),
                    "city": city,
                    "state": state,
                })
                
        return service_areas
        
    async def scrape_dumpster_sizes(self) -> List[Dict[str, Any]]:
        """Scrape dumpster sizes from Budget Dumpster"""
        html = await self.fetch_page(f"{self.base_url}/resources/dumpster-sizes")
        dumpster_sizes = []
        
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            size_elements = soup.find_all(string=re.compile(r'\d+\s*yard', re.IGNORECASE))
            
            for element in size_elements:
                size_match = re.search(r'(\d+)\s*yard', element, re.IGNORECASE)
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
                        "weight_limit_lbs": size * 250,  # Estimate weight limit based on size
                        "suitable_for": suitable_for
                    })
        
        if not dumpster_sizes:
            default_sizes = [
                (10, "10 yard dumpster for small projects and cleanouts", 2500, ["Small home projects", "Garage cleanouts", "Small remodeling projects"]),
                (15, "15 yard dumpster for medium residential projects", 3750, ["Medium home projects", "Basement cleanouts", "Small landscaping"]),
                (20, "20 yard dumpster for larger home renovation projects", 5000, ["Home renovations", "Medium construction", "Roofing projects"]),
                (30, "30 yard dumpster for major construction or renovation", 7500, ["Large construction", "Commercial projects", "Major home renovations"]),
                (40, "40 yard dumpster for large-scale projects", 10000, ["Large-scale demolition", "Commercial cleanouts", "Industrial projects"])
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
        """Scrape prices from Budget Dumpster"""
        
        service_areas = await self.scrape_service_areas()
        dumpster_sizes = await self.scrape_dumpster_sizes()
        prices = []
        
        for area in service_areas:
            for size in dumpster_sizes:
                base_price = 180 + (size["size_yards"] * 12)
                
                state_factor = 1.0
                if area["state"] in ["CA", "NY", "MA"]:
                    state_factor = 1.25  # Higher prices in expensive states
                elif area["state"] in ["TX", "FL", "GA"]:
                    state_factor = 0.85  # Lower prices in less expensive states
                
                adjusted_price = round(base_price * state_factor, 2)
                
                prices.append({
                    "id": str(uuid.uuid4()),
                    "company_id": self.company_id,
                    "size_id": size["id"],
                    "service_area_id": area["id"],
                    "base_price": adjusted_price,
                    "additional_day_price": round(adjusted_price * 0.12, 2),  # 12% of base price per additional day
                    "weight_overage_price": 65.0,  # $65 per ton over weight limit
                    "rental_period_days": 10  # Standard 10-day rental
                })
                
        return prices
