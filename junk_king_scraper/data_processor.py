import pandas as pd
import os
import logging
from datetime import datetime

logger = logging.getLogger("junk_king_scraper")

class DataProcessor:
    """
    Class for processing and validating scraped data.
    """
    def __init__(self, output_dir="data/output"):
        """
        Initialize the data processor.
        
        Args:
            output_dir (str): Directory to save output files
        """
        self.output_dir = output_dir
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def load_cities_data(self, csv_path):
        """
        Load cities data from CSV file.
        
        Args:
            csv_path (str): Path to the CSV file
            
        Returns:
            list: List of dictionaries containing city information
        """
        try:
            df = pd.read_csv(csv_path)
            logger.info(f"Loaded {len(df)} cities from {csv_path}")
            
            cities_data = df.to_dict('records')
            
            for city_data in cities_data:
                city_data["zip"] = str(city_data["zip"])
            
            return cities_data
            
        except Exception as e:
            logger.error(f"Error loading cities data from {csv_path}: {str(e)}")
            raise
    
    def validate_price(self, price):
        """
        Validate a price value.
        
        Args:
            price (str): Price value to validate
            
        Returns:
            tuple: (is_valid, cleaned_price)
        """
        if price is None or price == "N/A" or price == "ERROR":
            return True, price
        
        cleaned_price = ''.join(c for c in price if c.isdigit() or c == '.')
        
        try:
            price_float = float(cleaned_price)
            
            if 50 <= price_float <= 1000:
                return True, cleaned_price
            else:
                logger.warning(f"Price {price_float} is outside expected range (50-1000)")
                return False, cleaned_price
                
        except ValueError:
            logger.warning(f"Invalid price format: {price}")
            return False, "ERROR"
    
    def process_results(self, results):
        """
        Process and validate scraped results.
        
        Args:
            results (list): List of dictionaries containing scraped data
            
        Returns:
            pandas.DataFrame: Processed and validated data
        """
        df = pd.DataFrame(results)
        
        for index, row in df.iterrows():
            if row["status"] == "success":
                min_valid, min_price = self.validate_price(row["min_price"])
                full_valid, full_price = self.validate_price(row["full_price"])
                
                df.at[index, "min_price"] = min_price
                df.at[index, "full_price"] = full_price
                
                if not (min_valid and full_valid):
                    df.at[index, "status"] = "validation_error"
        
        logger.info(f"Processed {len(df)} results")
        logger.info(f"Success: {len(df[df['status'] == 'success'])}")
        logger.info(f"No service: {len(df[df['status'] == 'no_service'])}")
        logger.info(f"Error: {len(df[df['status'] == 'error'])}")
        logger.info(f"Validation error: {len(df[df['status'] == 'validation_error'])}")
        
        return df
    
    def save_results(self, df, include_timestamp=True):
        """
        Save processed results to CSV file.
        
        Args:
            df (pandas.DataFrame): Processed data
            include_timestamp (bool): Whether to include timestamp in filename
            
        Returns:
            str: Path to the saved file
        """
        if include_timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"junk_king_prices_{timestamp}.csv"
        else:
            month_year = datetime.now().strftime("%m%Y")
            filename = f"junk_king_prices_{month_year}.csv"
        
        file_path = os.path.join(self.output_dir, filename)
        
        df.to_csv(file_path, index=False)
        logger.info(f"Results saved to {file_path}")
        
        return file_path
    
    def generate_statistics(self, df):
        """
        Generate statistics from processed data.
        
        Args:
            df (pandas.DataFrame): Processed data
            
        Returns:
            dict: Dictionary containing statistics
        """
        stats = {
            "total": len(df),
            "success": len(df[df["status"] == "success"]),
            "no_service": len(df[df["status"] == "no_service"]),
            "error": len(df[df["status"] == "error"]) + len(df[df["status"] == "validation_error"]),
            "avg_min_price": None,
            "avg_full_price": None,
            "min_min_price": None,
            "max_min_price": None,
            "min_full_price": None,
            "max_full_price": None
        }
        
        success_df = df[df["status"] == "success"].copy()
        
        if len(success_df) > 0:
            success_df["min_price_numeric"] = pd.to_numeric(success_df["min_price"], errors="coerce")
            success_df["full_price_numeric"] = pd.to_numeric(success_df["full_price"], errors="coerce")
            
            stats["avg_min_price"] = success_df["min_price_numeric"].mean()
            stats["avg_full_price"] = success_df["full_price_numeric"].mean()
            stats["min_min_price"] = success_df["min_price_numeric"].min()
            stats["max_min_price"] = success_df["min_price_numeric"].max()
            stats["min_full_price"] = success_df["full_price_numeric"].min()
            stats["max_full_price"] = success_df["full_price_numeric"].max()
        
        return stats
