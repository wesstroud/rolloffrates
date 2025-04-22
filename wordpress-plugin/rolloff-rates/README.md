# RollOff Rates WordPress Plugin

A comprehensive WordPress plugin for displaying dumpster rental pricing and information from an external API. This plugin is designed to work with the RollOff Rates scraping backend to provide up-to-date dumpster rental pricing information for your WordPress site.

## Features

- **Dynamic Shortcodes**: Display dumpster rental pricing tables, company information, and lead forms using simple shortcodes
- **City-Specific Pages**: Generate SEO-optimized pages for each city in your service area
- **Static Page Generator**: Create static HTML pages for programmatic SEO at scale
- **Admin Dashboard**: Manage API settings, view lead submissions, and generate static pages
- **Responsive Design**: Mobile-friendly tables and forms that look great on all devices
- **Schema.org Markup**: Structured data for better search engine visibility
- **Caching System**: Efficient caching of API responses for improved performance

## Installation

1. Upload the `rolloff-rates` folder to the `/wp-content/plugins/` directory
2. Activate the plugin through the 'Plugins' menu in WordPress
3. Configure the plugin settings in the 'RollOff Rates' menu

## Configuration

1. Go to **RollOff Rates > Settings** in your WordPress admin
2. Enter your API URL (default: `https://api.rolloffrates.com`)
3. Configure cache duration and other settings
4. Save changes

## Usage

### Shortcodes

The plugin provides several shortcodes for displaying dumpster rental information:

#### Pricing Table

```
[rolloff_table city="Denver" state="CO"]
```

Displays a table of dumpster rental prices for the specified city.

#### Company List

```
[rolloff_companies city="Denver" state="CO" layout="grid"]
```

Displays a list of dumpster rental companies serving the specified city. The `layout` parameter can be `grid` or `list`.

#### Lead Form

```
[rolloff_form city="Denver" state="CO"]
```

Displays a lead generation form for the specified city.

### City Pages

The plugin can generate city-specific pages for each service area. To create a city page:

1. Go to **RollOff Rates > City Pages** in your WordPress admin
2. Click "Add New City Page"
3. Enter the city and state
4. Publish the page

### Static Page Generator

For programmatic SEO at scale, you can generate static HTML pages:

1. Go to **RollOff Rates > Static Generator** in your WordPress admin
2. Configure the output directory and base URL
3. Click "Generate Static Pages"

## External API Integration

This plugin is designed to work with the RollOff Rates API, which provides dumpster rental pricing and company information. The API should be hosted separately from your WordPress site, as recommended for performance and scalability.

The API should provide the following endpoints:

- `/api/cities` - List of all cities
- `/api/city/{city}/{state}` - Data for a specific city
- `/api/companies` - List of all companies
- `/api/dumpster-sizes` - List of all dumpster sizes
- `/api/prices` - List of all prices

## Development

### Prerequisites

- WordPress 5.6+
- PHP 7.4+
- External API for dumpster rental data

### Building from Source

1. Clone the repository
2. Install dependencies: `npm install`
3. Build assets: `npm run build`

## License

This plugin is licensed under the GPL v2 or later.

## Credits

Developed for RollOffRates.com
