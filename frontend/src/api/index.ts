import { Company, ServiceArea, DumpsterSize, DumpsterPrice, CityData } from '../types';

const API_URL = import.meta.env?.VITE_API_URL || 'http://localhost:8000';

export const fetchCompanies = async (): Promise<Company[]> => {
  try {
    const response = await fetch(`${API_URL}/companies`);
    if (!response.ok) {
      throw new Error('Failed to fetch companies');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching companies:', error);
    return [];
  }
};

export const fetchServiceAreas = async (): Promise<ServiceArea[]> => {
  try {
    const response = await fetch(`${API_URL}/service-areas`);
    if (!response.ok) {
      throw new Error('Failed to fetch service areas');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching service areas:', error);
    return [];
  }
};

export const fetchDumpsterSizes = async (): Promise<DumpsterSize[]> => {
  try {
    const response = await fetch(`${API_URL}/dumpster-sizes`);
    if (!response.ok) {
      throw new Error('Failed to fetch dumpster sizes');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching dumpster sizes:', error);
    return [];
  }
};

export const fetchPrices = async (): Promise<DumpsterPrice[]> => {
  try {
    const response = await fetch(`${API_URL}/prices`);
    if (!response.ok) {
      throw new Error('Failed to fetch prices');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching prices:', error);
    return [];
  }
};

export const fetchCities = async (): Promise<{ city: string; state: string }[]> => {
  try {
    const response = await fetch(`${API_URL}/cities`);
    if (!response.ok) {
      throw new Error('Failed to fetch cities');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching cities:', error);
    return [];
  }
};

export const fetchCityData = async (city: string, state?: string): Promise<CityData | null> => {
  try {
    const url = state 
      ? `${API_URL}/city/${encodeURIComponent(city)}?state=${encodeURIComponent(state)}`
      : `${API_URL}/city/${encodeURIComponent(city)}`;
    
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to fetch data for ${city}, ${state}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`Error fetching data for ${city}, ${state}:`, error);
    return null;
  }
};

export const triggerScrape = async (): Promise<{ message: string }> => {
  try {
    const response = await fetch(`${API_URL}/scrape`, {
      method: 'POST',
    });
    if (!response.ok) {
      throw new Error('Failed to trigger scrape');
    }
    return await response.json();
  } catch (error) {
    console.error('Error triggering scrape:', error);
    return { message: 'Failed to start scraping' };
  }
};
