import os
import asyncio
import pandas as pd
from playwright.async_api import async_playwright

async def main():
    """
    A simpler approach that uses Playwright to navigate the website and take screenshots
    for debugging purposes.
    """
    input_file = os.path.expanduser("~/attachments/f0516427-1bbc-4689-82a8-4b035baf7816/Roll+Off+Rates+Data+-+cities+1.csv")
    output_dir = os.path.expanduser("~/repos/rolloffrates/scraper/screenshots")
    
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.read_csv(input_file)
    
    if 'Full Address' not in df.columns and 'Address' in df.columns:
        address_column = 'Address'
    else:
        address_column = 'Full Address'
    
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
            await page.wait_for_selector("text=Home/Garage Cleanout", timeout=15000)
            await page.click("text=Home/Garage Cleanout")
            await page.screenshot(path=os.path.join(output_dir, "04_home_garage_selected.png"))
            
            print("Step 5: Selecting Mixed Household Trash")
            await page.wait_for_selector("text=Mixed Household Trash", timeout=15000)
            await page.click("text=Mixed Household Trash")
            await page.screenshot(path=os.path.join(output_dir, "05_mixed_trash_selected.png"))
            
            print("Step 6: Clicking Search button")
            search_button = await page.wait_for_selector("button:has-text('Search Available Dumpsters')", timeout=15000)
            await search_button.click()
            await page.screenshot(path=os.path.join(output_dir, "06_search_clicked.png"))
            
            print("Step 7: Waiting for results")
            await page.wait_for_selector("text=Choose the best dumpster size for your project", timeout=30000)
            await page.screenshot(path=os.path.join(output_dir, "07_results_loaded.png"))
            
            print("Step 8: Extracting dumpster data")
            
            html_content = await page.content()
            with open(os.path.join(output_dir, "results_page.html"), "w") as f:
                f.write(html_content)
            
            dumpster_cards = await page.query_selector_all("div.card, div[class*='dumpster-card']")
            print(f"Found {len(dumpster_cards)} dumpster cards")
            
            for i, card in enumerate(dumpster_cards):
                card_html = await page.evaluate("(element) => element.outerHTML", card)
                with open(os.path.join(output_dir, f"card_{i}.html"), "w") as f:
                    f.write(card_html)
                
                await card.screenshot(path=os.path.join(output_dir, f"card_{i}.png"))
                
                size_element = await card.query_selector("div:has-text('Yard')")
                price_element = await card.query_selector("span:has-text('$')")
                
                if size_element and price_element:
                    size = await size_element.text_content()
                    price = await price_element.text_content()
                    print(f"Card {i}: {size.strip()} - {price.strip()}")
            
        except Exception as e:
            print(f"Error: {str(e)}")
            await page.screenshot(path=os.path.join(output_dir, "error_state.png"))
        
        finally:
            await asyncio.sleep(5)
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
