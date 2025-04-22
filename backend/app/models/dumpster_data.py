from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class DumpsterCompany(BaseModel):
    """Model for dumpster rental companies"""
    id: str
    name: str
    website: str
    logo_url: Optional[str] = None
    description: Optional[str] = None
    phone: Optional[str] = None
    
class ServiceArea(BaseModel):
    """Model for service areas/cities"""
    id: str
    city: str
    state: str
    zip_code: Optional[str] = None
    county: Optional[str] = None
    
class DumpsterSize(BaseModel):
    """Model for dumpster sizes"""
    id: str
    company_id: str
    size_yards: int
    description: Optional[str] = None
    weight_limit_lbs: Optional[int] = None
    suitable_for: Optional[List[str]] = None
    
class DumpsterPrice(BaseModel):
    """Model for dumpster pricing"""
    id: str
    company_id: str
    size_id: str
    service_area_id: str
    base_price: float
    additional_day_price: Optional[float] = None
    weight_overage_price: Optional[float] = None
    rental_period_days: Optional[int] = None
    
class ScrapedData(BaseModel):
    """Model for storing all scraped data"""
    companies: List[DumpsterCompany] = []
    service_areas: List[ServiceArea] = []
    dumpster_sizes: List[DumpsterSize] = []
    prices: List[DumpsterPrice] = []
    last_updated: datetime = datetime.now()
