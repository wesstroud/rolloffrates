import { useState } from 'react';
import { Helmet } from 'react-helmet';
import { CitySelector } from './components/CitySelector';
import { CityPage } from './components/CityPage';
import { triggerScrape } from './api';
import './App.css';

function App() {
  const [selectedCity, setSelectedCity] = useState<{ city: string; state: string } | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const handleCitySelect = (city: string, state: string) => {
    setSelectedCity({ city, state });
  };

  const handleScrapeData = async () => {
    try {
      setIsLoading(true);
      setMessage('Scraping data from dumpster rental websites...');
      const result = await triggerScrape();
      setMessage(result.message);
    } catch (error) {
      setMessage('Error triggering data scrape. Please try again.');
      console.error('Error triggering scrape:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Helmet>
        <title>
          {selectedCity
            ? `Dumpster Rental in ${selectedCity.city}, ${selectedCity.state} - Best Prices & Services`
            : 'Dumpster Rental Services - Find the Best Prices in Your Area'}
        </title>
        <meta
          name="description"
          content={
            selectedCity
              ? `Compare dumpster rental prices and services in ${selectedCity.city}, ${selectedCity.state}. Find the best local providers for your waste management needs.`
              : 'Find affordable dumpster rental services in your area. Compare prices, sizes, and providers to get the best deal for your project.'
          }
        />
        {selectedCity && (
          <script type="application/ld+json">
            {`
              {
                "@context": "https://schema.org",
                "@type": "Service",
                "name": "Dumpster Rental in ${selectedCity.city}, ${selectedCity.state}",
                "description": "Compare dumpster rental prices and services in ${selectedCity.city}, ${selectedCity.state}. Find the best local providers for your waste management needs.",
                "areaServed": {
                  "@type": "City",
                  "name": "${selectedCity.city}",
                  "address": {
                    "@type": "PostalAddress",
                    "addressLocality": "${selectedCity.city}",
                    "addressRegion": "${selectedCity.state}",
                    "addressCountry": "US"
                  }
                },
                "provider": {
                  "@type": "LocalBusiness",
                  "name": "Dumpster Rental Comparison Service"
                }
              }
            `}
          </script>
        )}
      </Helmet>

      <header className="bg-white shadow-md">
        <div className="max-w-6xl mx-auto p-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-blue-600">Dumpster Rental Finder</h1>
            <button
              onClick={handleScrapeData}
              disabled={isLoading}
              className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition disabled:opacity-50"
            >
              {isLoading ? 'Scraping...' : 'Refresh Data'}
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto p-4 space-y-8">
        {message && (
          <div className="bg-blue-100 border-l-4 border-blue-500 text-blue-700 p-4 rounded">
            <p>{message}</p>
          </div>
        )}

        {!selectedCity ? (
          <>
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold mb-4">Find Dumpster Rental Services in Your Area</h2>
              <p className="text-xl text-gray-600">
                Compare prices and services from top dumpster rental companies in your city.
              </p>
            </div>
            <CitySelector onCitySelect={handleCitySelect} />
          </>
        ) : (
          <CityPage city={selectedCity.city} state={selectedCity.state} />
        )}
      </main>

      <footer className="bg-gray-800 text-white mt-12 py-8">
        <div className="max-w-6xl mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <h3 className="text-xl font-bold mb-4">Dumpster Rental Finder</h3>
              <p>
                Find the best dumpster rental services in your area. Compare prices, sizes, and providers to get the best deal for your project.
              </p>
            </div>
            <div>
              <h3 className="text-xl font-bold mb-4">Quick Links</h3>
              <ul className="space-y-2">
                <li>
                  <a href="#" className="hover:text-blue-300 transition">Home</a>
                </li>
                <li>
                  <a href="#" className="hover:text-blue-300 transition">About Us</a>
                </li>
                <li>
                  <a href="#" className="hover:text-blue-300 transition">Contact</a>
                </li>
                <li>
                  <a href="#" className="hover:text-blue-300 transition">Privacy Policy</a>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-xl font-bold mb-4">Contact Us</h3>
              <p>Email: info@dumpsterrentalfinder.com</p>
              <p>Phone: (800) 555-1234</p>
            </div>
          </div>
          <div className="border-t border-gray-700 mt-8 pt-8 text-center">
            <p>&copy; {new Date().getFullYear()} Dumpster Rental Finder. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
