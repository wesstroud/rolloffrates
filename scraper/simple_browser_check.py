import asyncio
from playwright.async_api import async_playwright

async def check_website():
    """Simple script to check if we can access the website and take screenshots"""
    async with async_playwright() as p:
        for browser_type in ['chromium', 'firefox']:
            print(f"\nTesting with {browser_type} browser...")
            
            browser = await getattr(p, browser_type).launch(
                headless=True,
                args=['--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage']
            )
            
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            )
            
            page = await context.new_page()
            
            try:
                print(f"Navigating to dumpsters.com/cart with {browser_type}...")
                await page.goto("https://www.dumpsters.com/cart", timeout=60000)
                print(f"Page loaded with {browser_type}")
                
                screenshot_path = f"dumpsters_com_cart_{browser_type}.png"
                await page.screenshot(path=screenshot_path)
                print(f"Screenshot saved to {screenshot_path}")
                
                html_content = await page.content()
                with open(f"dumpsters_com_cart_{browser_type}.html", "w") as f:
                    f.write(html_content)
                print(f"HTML content saved to dumpsters_com_cart_{browser_type}.html")
                
                title = await page.title()
                print(f"Page title: {title}")
                
                for selector in ["input[placeholder='Enter your address']", "input[type='text']", "form", "button"]:
                    elements = await page.query_selector_all(selector)
                    print(f"Found {len(elements)} elements matching '{selector}'")
                    
                    for i, element in enumerate(elements[:3]):
                        try:
                            tag_name = await page.evaluate("(element) => element.tagName", element)
                            element_html = await page.evaluate("(element) => element.outerHTML", element)
                            print(f"  Element {i}: {tag_name} - {element_html[:100]}...")
                        except:
                            print(f"  Element {i}: Could not get details")
            
            except Exception as e:
                print(f"Error with {browser_type}: {str(e)}")
            
            finally:
                await browser.close()

if __name__ == "__main__":
    asyncio.run(check_website())
