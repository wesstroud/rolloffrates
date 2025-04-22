# Deployment Instructions for RollOffRates.com

This document provides instructions for deploying the Dumpster Rental SEO Generator application to your GoDaddy-hosted domain RollOffRates.com.

## Prerequisites

1. GoDaddy hosting account with access to RollOffRates.com
2. SSH access to your GoDaddy hosting server (or FTP access)
3. Ability to configure DNS settings for your domain
4. Ability to set up subdomains (for API)

## Deployment Steps

### 1. Backend Deployment

The backend needs to be deployed to a server that can run Python applications. There are two main options:

#### Option A: Deploy on GoDaddy Hosting (if it supports Python/FastAPI)

1. Check if your GoDaddy hosting plan supports Python 3.9+ and the ability to run FastAPI applications
2. If supported, upload the entire `/backend` directory to your server
3. Install dependencies using Poetry: `poetry install`
4. Set up a production WSGI server like Gunicorn: `poetry add gunicorn`
5. Configure your server to run the FastAPI application using Gunicorn

#### Option B: Deploy on a Separate Cloud Provider (Recommended)

1. Create an account on a cloud provider that supports Python applications (AWS, DigitalOcean, Heroku, etc.)
2. Follow their specific deployment instructions for FastAPI applications
3. Deploy the backend code from the `/backend` directory
4. Configure the environment variables as needed
5. Set up a custom domain for your API: `api.rolloffrates.com`
6. Point this subdomain to your cloud provider using DNS settings in GoDaddy

### 2. Frontend Deployment

1. Log in to your GoDaddy hosting control panel
2. Navigate to the file manager for RollOffRates.com
3. Upload the contents of the `/frontend/dist` directory to the root directory of your website
4. Make sure the `index.html` file is in the root directory

### 3. DNS Configuration

1. Log in to your GoDaddy account
2. Navigate to the DNS management for RollOffRates.com
3. Set up an A record for the main domain to point to your GoDaddy hosting server
4. Set up a CNAME record for `api.rolloffrates.com` to point to your backend server

### 4. SSL Configuration

1. Enable SSL for both your main domain and the API subdomain
2. GoDaddy often provides free SSL certificates with hosting plans
3. Make sure both `https://rolloffrates.com` and `https://api.rolloffrates.com` are secured

## Testing the Deployment

1. Visit `https://rolloffrates.com` in your browser
2. Test the city selection functionality
3. Test the form submission
4. Check that all API calls are working correctly

## Troubleshooting

### Common Issues

1. **API Connection Errors**: Make sure the frontend is correctly configured to use `https://api.rolloffrates.com` as the API URL
2. **CORS Errors**: Ensure the backend CORS settings include your domain
3. **404 Errors**: Check that all files were uploaded correctly and that the server is configured to serve the SPA correctly

### Backend CORS Configuration

Make sure your backend's CORS settings include your domain:

```python
# In app/main.py
origins = [
    "https://rolloffrates.com",
    "https://www.rolloffrates.com",
    # Add any other domains that need to access the API
]
```

## Maintenance

1. To update the frontend, rebuild it and upload the new `dist` directory contents
2. To update the backend, deploy the new code to your backend server
3. To update the scraped data, set up a cron job to periodically run the scraping process

## Support

If you encounter any issues during deployment, please refer to:
- GoDaddy's hosting documentation
- FastAPI deployment documentation
- Your cloud provider's documentation for Python application deployment
