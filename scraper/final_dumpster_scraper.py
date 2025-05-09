import os
import asyncio
import re
import pandas as pd
from playwright.async_api import async_playwright

async def scrape_address(page, address):
    """Navigate to dumpsters.com and fill out the form with the given address"""
    try:
        await page.goto("https://www.dumpsters.com/cart", timeout=60000)
        print(f"Page loaded for {address}")
        
        try:
            await page.wait_for_selector("#address-search", timeout=10000)
            print(f"Address input found for {address}")
        except Exception as e:
            print(f"Could not find address input: {str(e)}")
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
        
        await asyncio.sleep(2)  # Add a small delay to ensure the page has updated
        
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
            return []
        
        await asyncio.sleep(2)  # Add a small delay to ensure the page has updated
        
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
            return []
        
        await asyncio.sleep(2)  # Add a small delay to ensure the page has updated
        
        try:
            await page.evaluate("""
                () => {
                    const buttons = Array.from(document.querySelectorAll('button'));
                    const searchButton = buttons.find(button => 
                        button.textContent.includes('Search Available Dumpsters') || 
                        button.textContent.includes('Search')
                    );
                    if (searchButton) searchButton.click();
                }
            """)
            print("Clicked search button using JavaScript")
        except Exception as e:
            print(f"JavaScript click failed: {str(e)}")
            
            try:
                await page.click("button:has-text('Search Available Dumpsters')")
                print("Clicked search button using direct selector")
            except Exception as e:
                print(f"Direct click failed: {str(e)}")
                return []
        
        await asyncio.sleep(5)  # Add a longer delay to ensure results have time to load
        
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
            return []
        
        dumpster_data = await extract_dumpster_data(page)
        
        return dumpster_data
    except Exception as e:
        print(f"Error processing address {address}: {str(e)}")
        return []

async def extract_dumpster_data(page):
    """Extract dumpster size and pricing information from the results page"""
    dumpster_data = []
    
    try:
        card_selectors = [
            "div.card", 
            "div[class*='dumpster-card']",
            "div:has-text('Yard'):has-text('$')"
        ]
        
        dumpster_cards = []
        for selector in card_selectors:
            cards = await page.query_selector_all(selector)
            if cards and len(cards) > 0:
                dumpster_cards = cards
                print(f"Found {len(cards)} dumpster cards using selector: {selector}")
                break
        
        if dumpster_cards and len(dumpster_cards) > 0:
            for i, card in enumerate(dumpster_cards):
                try:
                    card_html = await page.evaluate("(element) => element.outerHTML", card)
                    
                    size_match = re.search(r'(\d+)\s*Yard', card_html)
                    
                    price_match = re.search(r'\$(\d+)', card_html)
                    
                    if size_match and price_match:
                        size = f"{size_match.group(1)} Yard"
                        price = f"${price_match.group(1)}"
                        
                        print(f"Card {i}: {size} - {price}")
                        
                        dumpster_data.append({
                            "dumpster_size": size,
                            "price": price
                        })
                except Exception as e:
                    print(f"Error processing card {i}: {str(e)}")
        else:
            print("No cards found, trying direct extraction")
            
            content = await page.content()
            
            matches = re.findall(r'(\d+)\s*Yard.*?\$(\d+)', content, re.DOTALL)
            
            if matches:
                for size, price in matches:
                    print(f"Direct extraction: {size} Yard - ${price}")
                    dumpster_data.append({
                        "dumpster_size": f"{size} Yard",
                        "price": f"${price}"
                    })
            else:
                sizes = re.findall(r'(\d+)\s*Yard', content)
                prices = re.findall(r'\$(\d+)', content)
                
                prices = [p for p in prices if len(p) <= 4]  # Prices should be less than $10,000
                
                if sizes and prices and len(sizes) == len(prices):
                    for i in range(len(sizes)):
                        print(f"Matched extraction: {sizes[i]} Yard - ${prices[i]}")
                        dumpster_data.append({
                            "dumpster_size": f"{sizes[i]} Yard",
                            "price": f"${prices[i]}"
                        })
        
        unique_data = []
        seen = set()
        
        for item in dumpster_data:
            key = (item["dumpster_size"], item["price"])
            if key not in seen:
                seen.add(key)
                unique_data.append(item)
        
        return unique_data
    except Exception as e:
        print(f"Error extracting dumpster data: {str(e)}")
        return []

async def main():
    """Main function to scrape dumpster data for each address in the input file"""
    input_file = os.path.expanduser("~/attachments/f0516427-1bbc-4689-82a8-4b035baf7816/Roll+Off+Rates+Data+-+cities+1.csv")
    output_file = os.path.expanduser("~/repos/rolloffrates/scraper/dumpster_prices_final.csv")
    
    df = pd.read_csv(input_file)
    
    if 'Full Address' in df.columns:
        address_column = 'Full Address'
    else:
        address_column = 'Address'
    
    all_results = []
    
    sample_df = df.head(5)  # Process first 5 addresses for testing
    
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
        
        print("\nSample of results:")
        print(results_df.head())
    else:
        print("No results were collected.")

if __name__ == "__main__":
    asyncio.run(main())
