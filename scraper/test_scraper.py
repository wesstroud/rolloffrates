import os
from dumpsters_scraper import scrape_dumpsters

def test_with_sample():
    """Test the scraper with a small sample of addresses"""
    input_file = os.path.expanduser("~/attachments/f0516427-1bbc-4689-82a8-4b035baf7816/Roll+Off+Rates+Data+-+cities+1.csv")
    output_file = os.path.expanduser("~/repos/rolloffrates/scraper/test_results.csv")
    
    import pandas as pd
    df = pd.read_csv(input_file)
    sample_df = df.head(3)  # Just test with the first 3 addresses
    sample_file = os.path.expanduser("~/repos/rolloffrates/scraper/sample_addresses.csv")
    sample_df.to_csv(sample_file, index=False)
    
    print("Testing scraper with sample addresses...")
    scrape_dumpsters(sample_file, output_file)
    
    if os.path.exists(output_file):
        print(f"Test successful! Results saved to {output_file}")
        results_df = pd.read_csv(output_file)
        print("\nSample results:")
        print(results_df.head())
    else:
        print("Test failed: No output file was created.")

if __name__ == "__main__":
    test_with_sample()
