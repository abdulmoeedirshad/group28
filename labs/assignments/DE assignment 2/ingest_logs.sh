#!/bin/bash

DATE=$1
YEAR=$(date -d "$DATE" +%Y)
MONTH=$(date -d "$DATE" +%m)
DAY=$(date -d "$DATE" +%d)

# Define HDFS Paths
HDFS_LOG_DIR="/raw/logs/$YEAR/$MONTH/$DAY"
HDFS_METADATA_DIR="/raw/metadata"

# Local file paths (update based on actual location)
LOCAL_LOG_FILE="C:/Users/Hisham/user_logs.csv"
LOCAL_METADATA_FILE="C:/Users/Hisham/content_metadata.csv"

# Create HDFS directories
hdfs dfs -mkdir -p $HDFS_LOG_DIR
hdfs dfs -mkdir -p $HDFS_METADATA_DIR

# Copy files into HDFS
hdfs dfs -put -f $LOCAL_LOG_FILE $HDFS_LOG_DIR
hdfs dfs -put -f $LOCAL_METADATA_FILE $HDFS_METADATA_DIR

echo "Data successfully ingested into HDFS."


## ingestion script for cmd 
## wsl /mnt/c/Users/Hisham/Hive-project/ingest_logs.sh
