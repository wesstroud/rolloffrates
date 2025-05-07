import asyncio
from improved_regional_scraper import process_zip_codes

async def run_full_scraper():
    """Run the regional pricing scraper on the entire dataset."""
    input_file = "/home/ubuntu/attachments/6cb26970-af39-480f-9c18-20b37e1eb22d/Roll+Off+Rates+Data+-+Junk+King+Availability+1.csv"
    output_file = "/home/ubuntu/repos/rolloffrates/junk_king_regional_results.csv"
    
    print("Starting full scraper run with regional pricing model...")
    await process_zip_codes(input_file, output_file)
    print("Scraper completed successfully!")

if __name__ == "__main__":
    asyncio.run(run_full_scraper())
