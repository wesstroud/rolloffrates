import os
import time
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

def setup_driver():
    """Set up and return a headless Firefox driver"""
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    from selenium.webdriver.firefox.service import Service as FirefoxService
    
    options = FirefoxOptions()
    options.add_argument("--headless")
    
    driver = webdriver.Firefox(options=options)
    return driver

def fill_form(driver, address):
    """Navigate to dumpsters.com and fill out the form with the given address"""
    try:
        driver.get("https://www.dumpsters.com/cart")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Enter your address']"))
        )
        
        address_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your address']")
        address_input.clear()
        address_input.send_keys(address)
        
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".pac-container .pac-item"))
            )
            first_suggestion = driver.find_element(By.CSS_SELECTOR, ".pac-container .pac-item")
            first_suggestion.click()
        except (TimeoutException, NoSuchElementException):
            pass
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Home/Garage Cleanout')]"))
        )
        
        home_garage_option = driver.find_element(By.XPATH, "//div[contains(text(), 'Home/Garage Cleanout')]")
        home_garage_option.click()
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Mixed Household Trash')]"))
        )
        
        mixed_trash_option = driver.find_element(By.XPATH, "//div[contains(text(), 'Mixed Household Trash')]")
        mixed_trash_option.click()
        
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Search Available Dumpsters')]"))
        )
        search_button.click()
        
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Choose the best dumpster size for your project')]"))
        )
        
        return True
    except Exception as e:
        print(f"Error filling form for address {address}: {str(e)}")
        return False

def extract_dumpster_data(driver):
    """Extract dumpster size and pricing information from the results page"""
    dumpster_data = []
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='dumpster-size']"))
        )
        
        dumpster_elements = driver.find_elements(By.CSS_SELECTOR, "div[class*='dumpster-card']")
        
        if not dumpster_elements:
            dumpster_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'card') and .//div[contains(text(), 'Yard')]]")
        
        for element in dumpster_elements:
            try:
                size_element = element.find_element(By.XPATH, ".//div[contains(text(), 'Yard')]")
                size = size_element.text.strip()
                
                price_element = element.find_element(By.XPATH, ".//span[contains(text(), '$')]")
                price = price_element.text.strip()
                
                dumpster_data.append({
                    "dumpster_size": size,
                    "price": price
                })
            except NoSuchElementException:
                continue
        
        return dumpster_data
    except Exception as e:
        print(f"Error extracting dumpster data: {str(e)}")
        return []

def scrape_dumpsters(input_file, output_file):
    """Main function to scrape dumpster data for each address in the input file"""
    df = pd.read_csv(input_file)
    
    if 'Full Address' not in df.columns and 'Address' in df.columns:
        address_column = 'Address'
    else:
        address_column = 'Full Address'
    
    driver = setup_driver()
    
    all_results = []
    
    try:
        for index, row in df.iterrows():
            address = row[address_column]
            print(f"Processing address {index+1}/{len(df)}: {address}")
            
            if fill_form(driver, address):
                dumpster_data = extract_dumpster_data(driver)
                
                for data in dumpster_data:
                    all_results.append({
                        "address": address,
                        "dumpster_size": data["dumpster_size"],
                        "price": data["price"]
                    })
                
                print(f"Successfully scraped data for {address}")
            else:
                print(f"Failed to scrape data for {address}")
            
            time.sleep(2)
    finally:
        driver.quit()
    
    if all_results:
        results_df = pd.DataFrame(all_results)
        results_df.to_csv(output_file, index=False)
        print(f"Results saved to {output_file}")
    else:
        print("No results were collected.")

if __name__ == "__main__":
    input_file = os.path.expanduser("~/attachments/f0516427-1bbc-4689-82a8-4b035baf7816/Roll+Off+Rates+Data+-+cities+1.csv")
    output_file = os.path.expanduser("~/repos/rolloffrates/scraper/dumpster_prices.csv")
    
    scrape_dumpsters(input_file, output_file)
