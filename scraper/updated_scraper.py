import os
import time
import csv
import pandas as pd
import asyncio
from playwright.async_api import async_playwright

async def scrape_address(page, address):
    """Navigate to dumpsters.com and fill out the form with the given address"""
    try:
        await page.goto("https://www.dumpsters.com/cart", timeout=60000)
        print(f"Page loaded for {address}")
        
        await page.screenshot(path=f"debug_initial_{address.replace(' ', '_').replace(',', '')[:20]}.png")
        
        try:
            await page.wait_for_selector("#address-search", timeout=10000)
            print(f"Address input found for {address}")
        except Exception as e:
            print(f"Could not find address input: {str(e)}")
            await page.screenshot(path=f"error_address_input_{address.replace(' ', '_').replace(',', '')[:20]}.png")
            return []
        
        address_input = await page.query_selector("#address-search")
        await address_input.fill(address)
        print(f"Filled address: {address}")
        
        try:
            await page.wait_for_selector(".pac-container .pac-item", timeout=10000)
            await page.click(".pac-container .pac-item")
            print(f"Selected address suggestion for {address}")
        except Exception as e:
            print(f"No address suggestions or error: {str(e)}")
            await page.keyboard.press("Enter")
        
        await page.screenshot(path=f"debug_address_{address.replace(' ', '_').replace(',', '')[:20]}.png")
        
        try:
            selectors = [
                "text=Home/Garage Cleanout",
                "div:has-text('Home/Garage Cleanout')",
                "label:has-text('Home/Garage Cleanout')",
                "[data-value='Home/Garage Cleanout']"
            ]
            
            for selector in selectors:
                try:
                    await page.wait_for_selector(selector, timeout=5000)
                    await page.click(selector)
                    print(f"Selected Home/Garage Cleanout using selector: {selector}")
                    break
                except:
                    continue
            else:
                raise Exception("Could not find or click Home/Garage Cleanout option")
        except Exception as e:
            print(f"Could not select Home/Garage Cleanout option: {str(e)}")
            await page.screenshot(path=f"error_home_garage_{address.replace(' ', '_').replace(',', '')[:20]}.png")
            return []
        
        await page.screenshot(path=f"debug_home_garage_{address.replace(' ', '_').replace(',', '')[:20]}.png")
        
        try:
            selectors = [
                "text=Mixed Household Trash",
                "div:has-text('Mixed Household Trash')",
                "label:has-text('Mixed Household Trash')",
                "[data-value='Mixed Household Trash']"
            ]
            
            for selector in selectors:
                try:
                    await page.wait_for_selector(selector, timeout=5000)
                    await page.click(selector)
                    print(f"Selected Mixed Household Trash using selector: {selector}")
                    break
                except:
                    continue
            else:
                raise Exception("Could not find or click Mixed Household Trash option")
        except Exception as e:
            print(f"Could not select Mixed Household Trash option: {str(e)}")
            await page.screenshot(path=f"error_mixed_trash_{address.replace(' ', '_').replace(',', '')[:20]}.png")
            return []
        
        await page.screenshot(path=f"debug_mixed_trash_{address.replace(' ', '_').replace(',', '')[:20]}.png")
        
        try:
            button_selectors = [
                "button:has-text('Search Available Dumpsters')",
                "button:has-text('Search')",
                "button.search-button",
                "button[type='submit']"
            ]
            
            for selector in button_selectors:
                try:
                    search_button = await page.wait_for_selector(selector, timeout=5000)
                    if search_button:
                        await search_button.click()
                        print(f"Clicked Search button using selector: {selector}")
                        break
                except:
                    continue
            else:
                raise Exception("Could not find or click Search button")
        except Exception as e:
            print(f"Could not click Search button: {str(e)}")
            await page.screenshot(path=f"error_search_button_{address.replace(' ', '_').replace(',', '')[:20]}.png")
            return []
        
        await page.screenshot(path=f"debug_after_search_{address.replace(' ', '_').replace(',', '')[:20]}.png")
        
        try:
            result_selectors = [
                "text=Choose the best dumpster size for your project",
                "div:has-text('Choose the best dumpster size')",
                "div:has-text('Yard')",
                "div:has-text('$')"
            ]
            
            for selector in result_selectors:
                try:
                    await page.wait_for_selector(selector, timeout=10000)
                    print(f"Results loaded using selector: {selector}")
                    break
                except:
                    continue
            else:
                raise Exception("Could not find results page elements")
        except Exception as e:
            print(f"Could not load results: {str(e)}")
            await page.screenshot(path=f"error_results_{address.replace(' ', '_').replace(',', '')[:20]}.png")
            return []
        
        await page.screenshot(path=f"debug_results_{address.replace(' ', '_').replace(',', '')[:20]}.png")
        
        dumpster_data = await extract_dumpster_data(page, address)
        
        return dumpster_data
    except Exception as e:
        print(f"Error processing address {address}: {str(e)}")
        try:
            await page.screenshot(path=f"error_general_{address.replace(' ', '_').replace(',', '')[:20]}.png")
        except:
            pass
        return []

async def extract_dumpster_data(page, address):
    """Extract dumpster size and pricing information from the results page"""
    dumpster_data = []
    
    try:
        html_content = await page.content()
        with open(f"debug_html_{address.replace(' ', '_').replace(',', '')[:20]}.html", "w") as f:
            f.write(html_content)
        
        selectors = [
            "div.card", 
            "div[class*='dumpster-card']",
            "div:has-text('Yard'):has-text('$')",
            "div:has(div:has-text('Yard')):has(span:has-text('$'))"
        ]
        
        dumpster_elements = []
        for selector in selectors:
            elements = await page.query_selector_all(selector)
            if elements:
                dumpster_elements = elements
                print(f"Found {len(elements)} dumpster elements using selector: {selector}")
                break
        
        if not dumpster_elements:
            print(f"Could not find any dumpster elements for {address}")
            return []
        
        for i, element in enumerate(dumpster_elements):
            try:
                element_html = await page.evaluate("(element) => element.outerHTML", element)
                with open(f"debug_element_{i}_{address.replace(' ', '_').replace(',', '')[:20]}.html", "w") as f:
                    f.write(element_html)
                
                size_selectors = [
                    "div:has-text('Yard')",
                    "div[class*='size']",
                    "div:has-text('10 Yard'), div:has-text('15 Yard'), div:has-text('20 Yard'), div:has-text('30 Yard')"
                ]
                
                size = None
                for selector in size_selectors:
                    size_text = await element.query_selector(selector)
                    if size_text:
                        size = await size_text.text_content()
                        size = size.strip()
                        break
                
                price_selectors = [
                    "span:has-text('$')",
                    "div:has-text('$')",
                    "*:has-text('$')"
                ]
                
                price = None
                for selector in price_selectors:
                    price_text = await element.query_selector(selector)
                    if price_text:
                        price = await price_text.text_content()
                        price = price.strip()
                        break
                
                if size and price:
                    print(f"Found dumpster: {size} - {price}")
                    dumpster_data.append({
                        "dumpster_size": size,
                        "price": price
                    })
            except Exception as e:
                print(f"Error extracting data from dumpster element {i}: {str(e)}")
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
    
    sample_df = df.head(3)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage']
        )
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        page = await context.new_page()
        
        try:
            for index, row in sample_df.iterrows():
                address = row[address_column]
                print(f"\n\nProcessing address {index+1}/{len(sample_df)}: {address}")
                
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
                
                await asyncio.sleep(5)
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
