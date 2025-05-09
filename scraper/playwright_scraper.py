import os
import time
import csv
import pandas as pd
import asyncio
from playwright.async_api import async_playwright

async def scrape_address(page, address):
    """Navigate to dumpsters.com and fill out the form with the given address"""
    try:
        await page.goto("https://www.dumpsters.com/cart")
        
        await page.wait_for_selector("input[placeholder='Enter your address']")
        
        address_input = await page.query_selector("input[placeholder='Enter your address']")
        await address_input.fill(address)
        
        try:
            await page.wait_for_selector(".pac-container .pac-item", timeout=5000)
            await page.click(".pac-container .pac-item")
        except:
            pass
        
        await page.wait_for_selector("text=Home/Garage Cleanout")
        
        await page.click("text=Home/Garage Cleanout")
        
        await page.wait_for_selector("text=Mixed Household Trash")
        
        await page.click("text=Mixed Household Trash")
        
        await page.click("text=Search Available Dumpsters")
        
        await page.wait_for_selector("text=Choose the best dumpster size for your project", timeout=15000)
        
        dumpster_data = await extract_dumpster_data(page)
        
        return dumpster_data
    except Exception as e:
        print(f"Error processing address {address}: {str(e)}")
        return []

async def extract_dumpster_data(page):
    """Extract dumpster size and pricing information from the results page"""
    dumpster_data = []
    
    try:
        await page.wait_for_selector("div:has-text('Yard')")
        
        dumpster_elements = await page.query_selector_all("div.card, div[class*='dumpster-card']")
        
        for element in dumpster_elements:
            try:
                size_text = await element.query_selector("div:has-text('Yard')")
                if size_text:
                    size = await size_text.text_content()
                    size = size.strip()
                    
                    price_text = await element.query_selector("span:has-text('$')")
                    if price_text:
                        price = await price_text.text_content()
                        price = price.strip()
                        
                        dumpster_data.append({
                            "dumpster_size": size,
                            "price": price
                        })
            except Exception as e:
                print(f"Error extracting data from dumpster element: {str(e)}")
                continue
        
        return dumpster_data
    except Exception as e:
        print(f"Error extracting dumpster data: {str(e)}")
        return []

async def main():
    """Main function to scrape dumpster data for each address in the input file"""
    input_file = os.path.expanduser("~/attachments/f0516427-1bbc-4689-82a8-4b035baf7816/Roll+Off+Rates+Data+-+cities+1.csv")
    output_file = os.path.expanduser("~/repos/rolloffrates/scraper/dumpster_prices.csv")
    
    df = pd.read_csv(input_file)
    
    if 'Full Address' not in df.columns and 'Address' in df.columns:
        address_column = 'Address'
    else:
        address_column = 'Full Address'
    
    all_results = []
    
    sample_df = df.head(5)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            for index, row in sample_df.iterrows():
                address = row[address_column]
                print(f"Processing address {index+1}/{len(sample_df)}: {address}")
                
                dumpster_data = await scrape_address(page, address)
                
                for data in dumpster_data:
                    all_results.append({
                        "address": address,
                        "dumpster_size": data["dumpster_size"],
                        "price": data["price"]
                    })
                
                if dumpster_data:
                    print(f"Successfully scraped data for {address}")
                else:
                    print(f"No data found for {address}")
                
                await asyncio.sleep(2)
        finally:
            await browser.close()
    
    if all_results:
        results_df = pd.DataFrame(all_results)
        results_df.to_csv(output_file, index=False)
        print(f"Results saved to {output_file}")
    else:
        print("No results were collected.")

if __name__ == "__main__":
    asyncio.run(main())
