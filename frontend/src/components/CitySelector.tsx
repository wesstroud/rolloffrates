import { useState, useEffect } from 'react';
import { fetchCities } from '../api';

interface CitySelectorProps {
  onCitySelect: (city: string, state: string) => void;
}

export function CitySelector({ onCitySelect }: CitySelectorProps) {
  const [cities, setCities] = useState<{ city: string; state: string }[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedCity, setSelectedCity] = useState<{ city: string; state: string } | null>(null);

  useEffect(() => {
    const loadCities = async () => {
      try {
        setLoading(true);
        const citiesData = await fetchCities();
        setCities(citiesData);
        setError(null);
      } catch (err) {
        setError('Failed to load cities. Please try again later.');
        console.error('Error loading cities:', err);
      } finally {
        setLoading(false);
      }
    };

    loadCities();
  }, []);

  const handleCitySelect = (cityData: { city: string; state: string }) => {
    setSelectedCity(cityData);
    onCitySelect(cityData.city, cityData.state);
  };

  if (loading) {
    return <div className="p-4 text-center">Loading cities...</div>;
  }

  if (error) {
    return <div className="p-4 text-red-500 text-center">{error}</div>;
  }

  if (cities.length === 0) {
    return <div className="p-4 text-center">No cities available. Please trigger a data scrape first.</div>;
  }

  return (
    <div className="p-4 bg-white rounded-lg shadow-md">
      <h2 className="text-xl font-bold mb-4">Select a City</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {cities.map((cityData, index) => (
          <button
            key={index}
            className={`p-3 rounded-md border ${
              selectedCity?.city === cityData.city && selectedCity?.state === cityData.state
                ? 'bg-blue-100 border-blue-500'
                : 'bg-gray-50 border-gray-200 hover:bg-gray-100'
            }`}
            onClick={() => handleCitySelect(cityData)}
          >
            {cityData.city}, {cityData.state}
          </button>
        ))}
      </div>
    </div>
  );
}
