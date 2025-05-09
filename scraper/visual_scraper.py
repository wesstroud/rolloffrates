import os
import asyncio
import re
import pandas as pd
from playwright.async_api import async_playwright

async def main():
    """
    A visual browser scraper for debugging dumpsters.com
    """
    input_file = os.path.expanduser("~/attachments/f0516427-1bbc-4689-82a8-4b035baf7816/Roll+Off+Rates+Data+-+cities+1.csv")
    output_dir = os.path.expanduser("~/repos/rolloffrates/scraper/screenshots")
    
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.read_csv(input_file)
    
    if 'Full Address' in df.columns:
        address_column = 'Full Address'
    else:
        address_column = 'Address'
    
    address = df.iloc[0][address_column]
    print(f"Testing with address: {address}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,  # Use non-headless for debugging
            slow_mo=1000,    # Slow down actions for debugging
            args=['--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage']
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        
        page = await context.new_page()
        
        try:
            print("Step 1: Navigating to dumpsters.com/cart")
            await page.goto("https://www.dumpsters.com/cart", timeout=60000)
            await page.screenshot(path=os.path.join(output_dir, "01_initial_page.png"))
            
            print("Step 2: Filling in the address")
            await page.fill("#address-search", address)
            await page.screenshot(path=os.path.join(output_dir, "02_address_filled.png"))
            
            print("Step 3: Selecting address suggestion")
            try:
                await page.wait_for_selector(".pac-container .pac-item", timeout=10000)
                await page.click(".pac-container .pac-item")
                print("Selected address suggestion")
            except Exception as e:
                print(f"No address suggestions or error: {str(e)}")
                await page.keyboard.press("Enter")
            
            await page.screenshot(path=os.path.join(output_dir, "03_address_selected.png"))
            
            print("Step 4: Selecting Home/Garage Cleanout")
            await page.click("text=Home/Garage Cleanout")
            await page.screenshot(path=os.path.join(output_dir, "04_home_garage_selected.png"))
            
            print("Step 5: Selecting Mixed Household Trash")
            await page.click("text=Mixed Household Trash")
            await page.screenshot(path=os.path.join(output_dir, "05_mixed_trash_selected.png"))
            
            print("Step 6: Clicking Search button")
            await page.click("button:has-text('Search Available Dumpsters')")
            await page.screenshot(path=os.path.join(output_dir, "06_search_clicked.png"))
            
            print("Step 7: Waiting for results")
            await page.wait_for_selector("text=Choose the best dumpster size for your project", timeout=30000)
            await page.screenshot(path=os.path.join(output_dir, "07_results_loaded.png"))
            
            html_content = await page.content()
            with open(os.path.join(output_dir, "results_page.html"), "w") as f:
                f.write(html_content)
            
            print("Step 8: Extracting dumpster data")
            
            yard_elements = await page.query_selector_all("div:has-text('Yard')")
            print(f"Found {len(yard_elements)} elements with 'Yard' in their text")
            
            for i, el in enumerate(yard_elements[:10]):  # Limit to first 10 for brevity
                text = await el.text_content()
                print(f"Yard element {i}: {text.strip()}")
                
                await el.screenshot(path=os.path.join(output_dir, f"yard_element_{i}.png"))
            
            price_elements = await page.query_selector_all("span:has-text('$'), div:has-text('$')")
            print(f"Found {len(price_elements)} elements with '$' in their text")
            
            for i, el in enumerate(price_elements[:10]):  # Limit to first 10 for brevity
                text = await el.text_content()
                print(f"Price element {i}: {text.strip()}")
                
                await el.screenshot(path=os.path.join(output_dir, f"price_element_{i}.png"))
            
            print("Press Enter to close the browser...")
            await asyncio.sleep(30)
            
        except Exception as e:
            print(f"Error: {str(e)}")
            await page.screenshot(path=os.path.join(output_dir, "error_state.png"))
        
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
