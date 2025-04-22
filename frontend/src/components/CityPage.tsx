import { useState, useEffect } from 'react';
import { CityData, Company, DumpsterSize, DumpsterPrice } from '../types';
import { fetchCityData } from '../api';

interface CityPageProps {
  city: string;
  state: string;
}

export function CityPage({ city, state }: CityPageProps) {
  const [cityData, setCityData] = useState<CityData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    message: '',
  });

  useEffect(() => {
    const loadCityData = async () => {
      try {
        setLoading(true);
        const data = await fetchCityData(city, state);
        setCityData(data);
        setError(null);
      } catch (err) {
        setError(`Failed to load data for ${city}, ${state}. Please try again later.`);
        console.error(`Error loading data for ${city}, ${state}:`, err);
      } finally {
        setLoading(false);
      }
    };

    if (city && state) {
      loadCityData();
    }
  }, [city, state]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    alert(`Thank you for your inquiry! We'll contact you soon about dumpster rentals in ${city}, ${state}.`);
    setFormData({
      name: '',
      email: '',
      phone: '',
      message: '',
    });
  };

  const getLowestPriceByCompany = () => {
    if (!cityData) return [];

    const companyPrices: Record<string, { company: Company; price: number }> = {};

    cityData.prices.forEach((price) => {
      const company = cityData.companies.find((c) => c.id === price.company_id);
      if (company) {
        if (!companyPrices[company.id] || price.base_price < companyPrices[company.id].price) {
          companyPrices[company.id] = {
            company,
            price: price.base_price,
          };
        }
      }
    });

    return Object.values(companyPrices);
  };

  const getDumpsterSizesWithPrices = () => {
    if (!cityData) return [];

    const sizePrices: Record<string, { size: DumpsterSize; prices: DumpsterPrice[] }> = {};

    cityData.dumpster_sizes.forEach((size) => {
      const prices = cityData.prices.filter((p) => p.size_id === size.id);
      if (prices.length > 0) {
        sizePrices[size.id] = {
          size,
          prices: prices.sort((a, b) => a.base_price - b.base_price),
        };
      }
    });

    return Object.values(sizePrices);
  };

  if (loading) {
    return <div className="p-8 text-center">Loading data for {city}, {state}...</div>;
  }

  if (error) {
    return <div className="p-8 text-red-500 text-center">{error}</div>;
  }

  if (!cityData) {
    return <div className="p-8 text-center">No data available for {city}, {state}.</div>;
  }

  const lowestPricesByCompany = getLowestPriceByCompany();
  const dumpsterSizesWithPrices = getDumpsterSizesWithPrices();

  return (
    <div className="max-w-6xl mx-auto p-4">
      {/* SEO Metadata is handled in the head of the document */}
      
      {/* Hero Section */}
      <section className="bg-blue-600 text-white rounded-lg p-8 mb-8">
        <h1 className="text-4xl font-bold mb-4">Dumpster Rental in {city}, {state}</h1>
        <p className="text-xl mb-6">
          Find the best dumpster rental prices and services in {city}, {state}. Compare local providers and book today!
        </p>
        <div className="flex flex-wrap gap-4">
          <a 
            href="#contact" 
            className="bg-white text-blue-600 px-6 py-3 rounded-md font-semibold hover:bg-blue-50 transition"
          >
            Get a Quote
          </a>
          <a 
            href="tel:+18005551234" 
            className="bg-green-500 text-white px-6 py-3 rounded-md font-semibold hover:bg-green-600 transition flex items-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z" />
            </svg>
            Call Now
          </a>
        </div>
      </section>

      {/* Companies Section */}
      <section className="mb-12">
        <h2 className="text-3xl font-bold mb-6">Top Dumpster Rental Companies in {city}, {state}</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {lowestPricesByCompany.map(({ company, price }) => (
            <div key={company.id} className="border rounded-lg overflow-hidden shadow-md">
              <div className="p-6">
                <h3 className="text-xl font-bold mb-2">{company.name}</h3>
                <p className="text-gray-600 mb-4">{company.description}</p>
                <div className="flex justify-between items-center">
                  <div>
                    <span className="text-gray-500">Starting at</span>
                    <p className="text-2xl font-bold text-green-600">${price.toFixed(2)}</p>
                  </div>
                  {company.phone && (
                    <a 
                      href={`tel:${company.phone}`} 
                      className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition"
                    >
                      Call
                    </a>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Dumpster Sizes Section */}
      <section className="mb-12">
        <h2 className="text-3xl font-bold mb-6">Dumpster Sizes Available in {city}, {state}</h2>
        <div className="space-y-6">
          {dumpsterSizesWithPrices.map(({ size, prices }) => (
            <div key={size.id} className="border rounded-lg p-6 shadow-md">
              <h3 className="text-2xl font-bold mb-2">{size.size_yards} Yard Dumpster</h3>
              <p className="text-gray-600 mb-4">{size.description}</p>
              
              {size.suitable_for && size.suitable_for.length > 0 && (
                <div className="mb-4">
                  <h4 className="font-semibold mb-2">Suitable For:</h4>
                  <ul className="list-disc pl-5">
                    {size.suitable_for.map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                </div>
              )}
              
              <div className="flex justify-between items-center">
                <div>
                  <span className="text-gray-500">Price Range</span>
                  <p className="text-xl font-bold">
                    ${Math.min(...prices.map(p => p.base_price)).toFixed(2)} - 
                    ${Math.max(...prices.map(p => p.base_price)).toFixed(2)}
                  </p>
                </div>
                <a 
                  href="#contact" 
                  className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition"
                >
                  Get a Quote
                </a>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Contact Form Section */}
      <section id="contact" className="bg-gray-100 rounded-lg p-8">
        <h2 className="text-3xl font-bold mb-6">Get a Free Quote for Dumpster Rental in {city}, {state}</h2>
        <form onSubmit={handleSubmit} className="max-w-2xl">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label htmlFor="name" className="block text-gray-700 mb-2">Name</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border rounded-md"
                required
              />
            </div>
            <div>
              <label htmlFor="email" className="block text-gray-700 mb-2">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border rounded-md"
                required
              />
            </div>
          </div>
          <div className="mb-4">
            <label htmlFor="phone" className="block text-gray-700 mb-2">Phone</label>
            <input
              type="tel"
              id="phone"
              name="phone"
              value={formData.phone}
              onChange={handleInputChange}
              className="w-full px-4 py-2 border rounded-md"
              required
            />
          </div>
          <div className="mb-4">
            <label htmlFor="message" className="block text-gray-700 mb-2">Message</label>
            <textarea
              id="message"
              name="message"
              value={formData.message}
              onChange={handleInputChange}
              rows={4}
              className="w-full px-4 py-2 border rounded-md"
              placeholder="Tell us about your project and dumpster needs..."
              required
            ></textarea>
          </div>
          <button
            type="submit"
            className="bg-blue-600 text-white px-6 py-3 rounded-md font-semibold hover:bg-blue-700 transition"
          >
            Submit Request
          </button>
        </form>
      </section>
    </div>
  );
}
