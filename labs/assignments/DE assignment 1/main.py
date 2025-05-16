import os
from reddit_data_collection import main as fetch_reddit
from google_trends_data import main as fetch_trends
from public_data_processing import main as fetch_public_data

def create_directory_structure():
    ##Creating necessary directories for storing data.
    os.makedirs("datasets/raw", exist_ok=True)
    os.makedirs("datasets/processed", exist_ok=True)

def main():
    """Run the full data pipeline."""
    print("Starting data collection pipeline")
    
    create_directory_structure()
    fetch_reddit()
    fetch_trends()
    fetch_public_data()
    
    print("Data collection pipeline completed successfully")

if __name__ == "__main__":
    main()
