# Dumpster Rental SEO Generator

A full-stack application for programmatic SEO targeting dumpster rental services. This application scrapes data from multiple national dumpster rental websites, stores the data in a structured JSON format, and generates SEO-optimized pages for each city or service area. The application helps improve online visibility for dumpster rental businesses.

## Features

- Web scrapers for multiple dumpster rental websites (Waste Management, Budget Dumpster)
- Structured JSON data storage with comprehensive data models
- Dynamic SEO page generation for each city/service area
- SEO metadata (title tags, meta descriptions, schema.org markup)
- Lead generation form and click-to-call functionality
- Responsive design with Tailwind CSS

## Project Structure

```
dumpster-seo-generator/
├── backend/                # FastAPI backend
│   ├── app/
│   │   ├── main.py         # Main application entry point
│   │   ├── models/         # Data models
│   │   ├── scrapers/       # Web scrapers
│   │   └── utils/          # Utility functions
│   ├── data/               # Scraped data storage
│   ├── Dockerfile          # Backend Docker configuration
│   └── pyproject.toml      # Poetry dependencies
├── frontend/               # React frontend
│   ├── dist/               # Production build
│   ├── public/             # Static assets
│   ├── src/
│   │   ├── api/            # API client
│   │   ├── components/     # React components
│   │   └── types/          # TypeScript type definitions
│   ├── .env                # Environment variables
│   └── package.json        # NPM dependencies
├── docker-compose.yml      # Docker Compose configuration
├── nginx.conf              # Nginx configuration for production
├── DEPLOYMENT.md           # Detailed deployment instructions
└── README.md               # Project documentation
```

## Local Development

### Backend

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install dependencies using Poetry:
   ```
   poetry install
   ```

3. Start the development server:
   ```
   poetry run fastapi dev app/main.py
   ```

4. The API will be available at http://localhost:8000

### Frontend

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run dev
   ```

4. The frontend will be available at http://localhost:5173

## Deployment

This application is configured for deployment to RollOffRates.com via GoDaddy hosting. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### Quick Deployment Steps

1. Build the frontend:
   ```
   cd frontend
   npm run build
   ```

2. Deploy the backend to a server that supports Python/FastAPI

3. Update the frontend `.env` file with the production API URL:
   ```
   VITE_API_URL=https://api.rolloffrates.com
   ```

4. Upload the frontend build files to your GoDaddy hosting

5. Configure DNS settings for your domain

## Data Scraping

The application includes scrapers for the following dumpster rental websites:

- Waste Management
- Budget Dumpster

To trigger a data scrape, use the `/scrape` endpoint of the API.

## License

This project is proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.
