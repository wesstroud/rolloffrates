import os
import asyncio
import pandas as pd
from playwright.async_api import async_playwright

async def main():
    """
    A headless browser scraper with improved debugging for dumpsters.com
    """
    input_file = os.path.expanduser("~/attachments/f0516427-1bbc-4689-82a8-4b035baf7816/Roll+Off+Rates+Data+-+cities+1.csv")
    output_dir = os.path.expanduser("~/repos/rolloffrates/scraper/screenshots")
    output_file = os.path.expanduser("~/repos/rolloffrates/scraper/dumpster_prices.csv")
    
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.read_csv(input_file)
    
    if 'Full Address' not in df.columns and 'Address' in df.columns:
        address_column = 'Address'
    else:
        address_column = 'Full Address'
    
    sample_df = df.head(3)
    
    all_results = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,  # Must use headless in this environment
            args=['--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage']
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        
        page = await context.new_page()
        
        for index, row in sample_df.iterrows():
            address = row[address_column]
            print(f"\n\nProcessing address {index+1}/{len(sample_df)}: {address}")
            
            try:
                print("Step 1: Navigating to dumpsters.com/cart")
                response = await page.goto("https://www.dumpsters.com/cart", timeout=60000)
                print(f"Navigation status: {response.status}")
                await page.screenshot(path=os.path.join(output_dir, f"{index+1}_01_initial_page.png"))
                
                html_content = await page.content()
                with open(os.path.join(output_dir, f"{index+1}_initial_page.html"), "w") as f:
                    f.write(html_content)
                
                print("Step 2: Filling in the address")
                address_input = await page.query_selector("#address-search")
                if address_input:
                    await address_input.fill(address)
                    print("Address input filled")
                else:
                    print("Could not find address input field")
                    for selector in ["input[type='text']", "input.autocomplete--active", "input[name='search']"]:
                        address_input = await page.query_selector(selector)
                        if address_input:
                            await address_input.fill(address)
                            print(f"Address input filled using selector: {selector}")
                            break
                
                await page.screenshot(path=os.path.join(output_dir, f"{index+1}_02_address_filled.png"))
                
                print("Step 3: Selecting address suggestion")
                try:
                    await page.wait_for_selector(".pac-container .pac-item", timeout=10000)
                    await page.click(".pac-container .pac-item")
                    print("Selected address suggestion")
                except Exception as e:
                    print(f"No address suggestions or error: {str(e)}")
                    await page.keyboard.press("Enter")
                
                await page.screenshot(path=os.path.join(output_dir, f"{index+1}_03_address_selected.png"))
                
                html_content = await page.content()
                with open(os.path.join(output_dir, f"{index+1}_after_address_selection.html"), "w") as f:
                    f.write(html_content)
                
                print("Step 4: Looking for Home/Garage Cleanout option")
                
                options = await page.query_selector_all("div.option, label.option, div[role='button']")
                print(f"Found {len(options)} potential option elements")
                
                for i, option in enumerate(options[:5]):  # Limit to first 5 for brevity
                    try:
                        text = await option.text_content()
                        print(f"Option {i}: {text.strip()}")
                    except:
                        print(f"Option {i}: Could not get text")
                
                home_garage_selectors = [
                    "text=Home/Garage Cleanout",
                    "div:has-text('Home/Garage Cleanout')",
                    "label:has-text('Home/Garage Cleanout')",
                    "[data-value='Home/Garage Cleanout']"
                ]
                
                for selector in home_garage_selectors:
                    try:
                        element = await page.query_selector(selector)
                        if element:
                            await element.click()
                            print(f"Clicked Home/Garage Cleanout using selector: {selector}")
                            break
                    except Exception as e:
                        print(f"Could not click using selector {selector}: {str(e)}")
                
                await page.screenshot(path=os.path.join(output_dir, f"{index+1}_04_home_garage_selected.png"))
                
                html_content = await page.content()
                with open(os.path.join(output_dir, f"{index+1}_after_home_garage_selection.html"), "w") as f:
                    f.write(html_content)
                
                print("Step 5: Looking for Mixed Household Trash option")
                
                options = await page.query_selector_all("div.option, label.option, div[role='button']")
                print(f"Found {len(options)} potential option elements")
                
                for i, option in enumerate(options[:5]):  # Limit to first 5 for brevity
                    try:
                        text = await option.text_content()
                        print(f"Option {i}: {text.strip()}")
                    except:
                        print(f"Option {i}: Could not get text")
                
                mixed_trash_selectors = [
                    "text=Mixed Household Trash",
                    "div:has-text('Mixed Household Trash')",
                    "label:has-text('Mixed Household Trash')",
                    "[data-value='Mixed Household Trash']"
                ]
                
                for selector in mixed_trash_selectors:
                    try:
                        element = await page.query_selector(selector)
                        if element:
                            await element.click()
                            print(f"Clicked Mixed Household Trash using selector: {selector}")
                            break
                    except Exception as e:
                        print(f"Could not click using selector {selector}: {str(e)}")
                
                await page.screenshot(path=os.path.join(output_dir, f"{index+1}_05_mixed_trash_selected.png"))
                
                html_content = await page.content()
                with open(os.path.join(output_dir, f"{index+1}_after_mixed_trash_selection.html"), "w") as f:
                    f.write(html_content)
                
                print("Step 6: Looking for Search button")
                
                buttons = await page.query_selector_all("button")
                print(f"Found {len(buttons)} button elements")
                
                for i, button in enumerate(buttons[:5]):  # Limit to first 5 for brevity
                    try:
                        text = await button.text_content()
                        print(f"Button {i}: {text.strip()}")
                    except:
                        print(f"Button {i}: Could not get text")
                
                search_button_selectors = [
                    "button:has-text('Search Available Dumpsters')",
                    "button:has-text('Search')",
                    "button.search-button",
                    "button[type='submit']",
                    "button.btn-primary"
                ]
                
                for selector in search_button_selectors:
                    try:
                        button = await page.query_selector(selector)
                        if button:
                            await button.click()
                            print(f"Clicked Search button using selector: {selector}")
                            break
                    except Exception as e:
                        print(f"Could not click using selector {selector}: {str(e)}")
                
                await page.screenshot(path=os.path.join(output_dir, f"{index+1}_06_search_clicked.png"))
                
                html_content = await page.content()
                with open(os.path.join(output_dir, f"{index+1}_after_search_click.html"), "w") as f:
                    f.write(html_content)
                
                print("Step 7: Waiting for results")
                try:
                    await page.wait_for_selector("text=Choose the best dumpster size for your project", timeout=30000)
                    print("Results page loaded")
                except Exception as e:
                    print(f"Could not detect results page: {str(e)}")
                
                await page.screenshot(path=os.path.join(output_dir, f"{index+1}_07_results_loaded.png"))
                
                html_content = await page.content()
                with open(os.path.join(output_dir, f"{index+1}_results_page.html"), "w") as f:
                    f.write(html_content)
                
                print("Step 8: Extracting dumpster data")
                
                card_selectors = [
                    "div.card", 
                    "div[class*='dumpster-card']",
                    "div:has-text('Yard'):has-text('$')",
                    "div:has(div:has-text('Yard')):has(span:has-text('$'))"
                ]
                
                dumpster_cards = []
                for selector in card_selectors:
                    cards = await page.query_selector_all(selector)
                    if cards:
                        dumpster_cards = cards
                        print(f"Found {len(cards)} dumpster cards using selector: {selector}")
                        break
                
                if not dumpster_cards:
                    print("Could not find any dumpster cards")
                
                dumpster_data = []
                for i, card in enumerate(dumpster_cards):
                    try:
                        card_html = await page.evaluate("(element) => element.outerHTML", card)
                        with open(os.path.join(output_dir, f"{index+1}_card_{i}.html"), "w") as f:
                            f.write(card_html)
                        
                        size_element = await card.query_selector("div:has-text('Yard')")
                        price_element = await card.query_selector("span:has-text('$')")
                        
                        if size_element and price_element:
                            size = await size_element.text_content()
                            price = await price_element.text_content()
                            print(f"Card {i}: {size.strip()} - {price.strip()}")
                            
                            dumpster_data.append({
                                "dumpster_size": size.strip(),
                                "price": price.strip()
                            })
                    except Exception as e:
                        print(f"Error processing card {i}: {str(e)}")
                
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
                
            except Exception as e:
                print(f"Error processing address {address}: {str(e)}")
                await page.screenshot(path=os.path.join(output_dir, f"{index+1}_error_state.png"))
        
        await browser.close()
    
    if all_results:
        results_df = pd.DataFrame(all_results)
        results_df.to_csv(output_file, index=False)
        print(f"Results saved to {output_file}")
    else:
        print("No results were collected.")

if __name__ == "__main__":
    asyncio.run(main())
