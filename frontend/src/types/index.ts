export interface Company {
  id: string;
  name: string;
  website: string;
  logo_url?: string;
  description?: string;
  phone?: string;
}

export interface ServiceArea {
  id: string;
  city: string;
  state: string;
  zip_code?: string;
  county?: string;
}

export interface DumpsterSize {
  id: string;
  company_id: string;
  size_yards: number;
  description?: string;
  weight_limit_lbs?: number;
  suitable_for?: string[];
}

export interface DumpsterPrice {
  id: string;
  company_id: string;
  size_id: string;
  service_area_id: string;
  base_price: number;
  additional_day_price?: number;
  weight_overage_price?: number;
  rental_period_days?: number;
}

export interface CityData {
  service_areas: ServiceArea[];
  companies: Company[];
  dumpster_sizes: DumpsterSize[];
  prices: DumpsterPrice[];
}
