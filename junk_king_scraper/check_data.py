import pandas as pd
import os

def check_csv_data(csv_path):
    """
    Check if the CSV file is loaded correctly and print basic statistics.
    """
    print(f"Checking CSV file: {csv_path}")
    
    if not os.path.exists(csv_path):
        print(f"Error: File {csv_path} does not exist!")
        return
    
    try:
        df = pd.read_csv(csv_path)
        print(f"Successfully loaded CSV file with {len(df)} rows.")
        
        print("\nColumns in the CSV file:")
        for col in df.columns:
            print(f"- {col}")
        
        print("\nSample data (first 5 rows):")
        print(df.head())
        
        print("\nStates distribution:")
        state_counts = df['state'].value_counts()
        for state, count in state_counts.items():
            print(f"- {state}: {count} cities")
        
        print("\nAll cities have availability:", all(df['is_available'] == True))
        
    except Exception as e:
        print(f"Error loading CSV file: {str(e)}")

if __name__ == "__main__":
    check_csv_data("data/cities.csv")
