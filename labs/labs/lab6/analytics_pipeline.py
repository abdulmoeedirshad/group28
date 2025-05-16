import pandas as pd
import matplotlib.pyplot as plt
from prefect import task, flow, get_run_logger

@task
def fetch_data():
    logger = get_run_logger()
    logger.info("Reading data...")
    df = pd.read_csv(r"C:\Users\hisha\LUMS\Data Engenering\lab6\analytics_data.csv")
    logger.info(f"Data shape: {df.shape}")
    return df

@task
def validate_data(df):
    logger = get_run_logger()
    logger.info("Validating data...")
    missing_values = df.isnull().sum()
    logger.info(f"Missing values:\n{missing_values}")
    df_clean = df.dropna()
    return df_clean

@task
def transform_data(df):
    logger = get_run_logger()
    logger.info("Transforming data...")
    if "sales" in df.columns:
        df["sales_normalized"] = (df["sales"] - df["sales"].mean()) / df["sales"].std()
    return df

@task
def generate_report(df):
    logger = get_run_logger()
    logger.info("Generating analytics report...")
    summary = df.describe()
    summary.to_csv("data_analytics_summary.csv")
    logger.info("Summary statistics saved to data/analytics_summary.csv")

@task
def create_histogram(df):
    logger = get_run_logger()
    if "sales" in df.columns:
        plt.hist(df["sales"], bins=20)
        plt.title("Sales Distribution")
        plt.xlabel("Sales")
        plt.ylabel("Frequency")
        plt.savefig("data_sales_histogram.png")
        plt.close()
        logger.info("Sales histogram saved to data/sales_histogram.png")

@flow
def analytics_pipeline():
    df = fetch_data()
    df_clean = validate_data(df)
    df_transformed = transform_data(df_clean)
    generate_report(df_transformed)
    create_histogram(df_transformed)
    
if __name__ == "__main__":
    analytics_pipeline()
