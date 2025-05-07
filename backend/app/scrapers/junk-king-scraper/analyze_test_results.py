import pandas as pd
import os

def analyze_test_results():
    """Analyze the test results from the regional pricing scraper."""
    test_results_file = "/home/ubuntu/repos/rolloffrates/junk_king_regional_test_results.csv"
    
    if not os.path.exists(test_results_file):
        print("Test results file not found.")
        return
    
    df = pd.read_csv(test_results_file)
    
    print(f"Total records processed: {len(df)}")
    
    available_count = df['is_available'].sum()
    print(f"Available locations: {available_count} ({available_count/len(df)*100:.2f}%)")
    
    available_df = df[df['is_available'] == True]
    if len(available_df) > 0:
        available_df['min_price_numeric'] = available_df['min_price'].str.replace('$', '').astype(float)
        available_df['max_price_numeric'] = available_df['max_price'].str.replace('$', '').astype(float)
        
        print("\nPricing statistics:")
        print(f"Min price range: ${available_df['min_price_numeric'].min()} - ${available_df['min_price_numeric'].max()}")
        print(f"Max price range: ${available_df['max_price_numeric'].min()} - ${available_df['max_price_numeric'].max()}")
        print(f"Average min price: ${available_df['min_price_numeric'].mean():.2f}")
        print(f"Average max price: ${available_df['max_price_numeric'].mean():.2f}")
        
        print("\nPrice ranges by state:")
        for state in available_df['state'].unique():
            state_df = available_df[available_df['state'] == state]
            min_prices = state_df['min_price_numeric']
            max_prices = state_df['max_price_numeric']
            
            print(f"{state}:")
            print(f"  Min price range: ${min_prices.min()} - ${min_prices.max()}")
            print(f"  Max price range: ${max_prices.min()} - ${max_prices.max()}")
            print(f"  Average min price: ${min_prices.mean():.2f}")
            print(f"  Average max price: ${max_prices.mean():.2f}")
        
        print("\nPrice comparison for major cities vs. other cities:")
        major_cities = ['New York City', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 
                        'Philadelphia', 'San Antonio', 'San Diego', 'Dallas']
        
        major_city_df = available_df[available_df['city'].isin(major_cities)]
        other_city_df = available_df[~available_df['city'].isin(major_cities)]
        
        if len(major_city_df) > 0:
            print("Major Cities:")
            print(f"  Average min price: ${major_city_df['min_price_numeric'].mean():.2f}")
            print(f"  Average max price: ${major_city_df['max_price_numeric'].mean():.2f}")
        
        if len(other_city_df) > 0:
            print("Other Cities:")
            print(f"  Average min price: ${other_city_df['min_price_numeric'].mean():.2f}")
            print(f"  Average max price: ${other_city_df['max_price_numeric'].mean():.2f}")

if __name__ == "__main__":
    analyze_test_results()
