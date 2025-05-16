import pandas as pd
import os

def load_public_dataset(url, output_filename):
    df = pd.read_csv(url)
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    df.to_csv(output_filename, index=False)
    return df

def summarize_dataset(df):
    print(df.info())
    print(df.describe())

def main():
    dataset_url = "https://data.ct.gov/api/views/jfhb-ebu6/rows.csv?accessType=DOWNLOAD"  # source: https://catalog.data.gov/dataset/electric-vehicle-population-data
    output_file = "datasets/raw/public_ev_charging_data.csv"
    
    df = load_public_dataset(dataset_url, output_file)
    print("Public dataset saved successfully.")
    summarize_dataset(df)
    
if __name__ == "__main__":
    main()
