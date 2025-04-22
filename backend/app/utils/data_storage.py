import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
import logging

from ..models.dumpster_data import ScrapedData

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataStorage:
    """Class for storing and retrieving scraped data"""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize the data storage with a directory path"""
        self.data_dir = data_dir
        self.data_file = os.path.join(data_dir, "dumpster_data.json")
        
        os.makedirs(data_dir, exist_ok=True)
        
        if not os.path.exists(self.data_file):
            self.save_data(ScrapedData())
    
    def save_data(self, data: ScrapedData) -> bool:
        """Save data to JSON file"""
        try:
            data.last_updated = datetime.now()
            
            with open(self.data_file, 'w') as f:
                json.dump(data.dict(), f, default=str, indent=2)
            
            logger.info(f"Data saved successfully to {self.data_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
            return False
    
    def load_data(self) -> ScrapedData:
        """Load data from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data_dict = json.load(f)
                
                if 'last_updated' in data_dict and isinstance(data_dict['last_updated'], str):
                    data_dict['last_updated'] = datetime.fromisoformat(data_dict['last_updated'].replace('Z', '+00:00'))
                
                return ScrapedData(**data_dict)
            else:
                logger.warning(f"Data file {self.data_file} not found. Returning empty data.")
                return ScrapedData()
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return ScrapedData()
    
    def update_data(self, new_data: Dict[str, Any]) -> bool:
        """Update existing data with new data"""
        try:
            current_data = self.load_data()
            
            if 'companies' in new_data:
                current_data.companies.extend(new_data['companies'])
            
            if 'service_areas' in new_data:
                current_data.service_areas.extend(new_data['service_areas'])
            
            if 'dumpster_sizes' in new_data:
                current_data.dumpster_sizes.extend(new_data['dumpster_sizes'])
            
            if 'prices' in new_data:
                current_data.prices.extend(new_data['prices'])
            
            return self.save_data(current_data)
        except Exception as e:
            logger.error(f"Error updating data: {str(e)}")
            return False
    
    def get_service_areas(self) -> list:
        """Get all service areas"""
        data = self.load_data()
        return data.service_areas
    
    def get_companies(self) -> list:
        """Get all companies"""
        data = self.load_data()
        return data.companies
    
    def get_dumpster_sizes(self) -> list:
        """Get all dumpster sizes"""
        data = self.load_data()
        return data.dumpster_sizes
    
    def get_prices(self) -> list:
        """Get all prices"""
        data = self.load_data()
        return data.prices
    
    def get_data_for_city(self, city: str, state: Optional[str] = None) -> Dict[str, Any]:
        """Get all data for a specific city"""
        data = self.load_data()
        
        matching_areas = []
        for area in data.service_areas:
            if area.city.lower() == city.lower():
                if state is None or area.state.lower() == state.lower():
                    matching_areas.append(area)
        
        if not matching_areas:
            return {}
        
        area_ids = [area.id for area in matching_areas]
        matching_prices = [price for price in data.prices if price.service_area_id in area_ids]
        
        company_ids = set(price.company_id for price in matching_prices)
        size_ids = set(price.size_id for price in matching_prices)
        
        matching_companies = [company for company in data.companies if company.id in company_ids]
        matching_sizes = [size for size in data.dumpster_sizes if size.id in size_ids]
        
        return {
            "service_areas": matching_areas,
            "companies": matching_companies,
            "dumpster_sizes": matching_sizes,
            "prices": matching_prices
        }
