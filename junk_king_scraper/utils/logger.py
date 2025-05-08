import logging
import os
from datetime import datetime

def setup_logger(log_dir="logs"):
    """
    Configure and return a logger for the application.
    Creates rotating log files with timestamps.
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logger = logging.getLogger("junk_king_scraper")
    logger.setLevel(logging.INFO)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"scraper_{timestamp}.log")
    file_handler = logging.FileHandler(log_file)
    
    console_handler = logging.StreamHandler()
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
