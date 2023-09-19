import os
import boto3
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# Initialize the S3 client
s3_client = boto3.client('s3')

# Specify your bucket name and folder paths
source_bucket = 'mybuckets'
source_folder = 'The_Pile_txt/'
destination_folder = 'The_Pile_txt_cloned'

# Create thread pool with 4 worker threads
executor = ThreadPoolExecutor(max_workers=4)

def estimate_rows_for_chunksize(sample_df, target_chunk_size_in_MB=25):
    avg_row_size = sample_df.memory_usage(index=True, deep=True).sum() / len(sample_df)  # average size in bytes
    avg_row_size_MB = avg_row_size / (1024 * 1024)  # convert to MB
    estimated_rows = int(target_chunk_size_in_MB / avg_row_size_MB)
    return estimated_rows

def download_file(bucket, src_key, dst_file_path):
    try:
        s3_client.download_file(bucket, src_key, dst_file_path)
    except Exception as e:
        print(f"Error downloading file: {e}")

def upload_file(bucket, src_file_path, dst_key):
    try:
        s3_client.upload_file(src_file_path, bucket, dst_key)
    except Exception as e:
        print(f"Error uploading file: {e}")

def split_and_upload_csv(file_path, bucket, destination_folder):
    try:
        # Estimate chunk size
        sample_df = pd.read_csv(file_path, nrows=100)
        estimated_chunksize = estimate_rows_for_chunksize(sample_df)
        
        base_name = os.path.basename(file_path).replace('.csv', '')
        for i, chunk in enumerate(pd.read_csv(file_path, chunksize=estimated_chunksize)):
            chunk_file_path = f"{base_name}_chunk_{i}.csv"
            chunk.to_csv(chunk_file_path, index=False)

            # Upload to S3
            dst_key = os.path.join(destination_folder, chunk_file_path)
            upload_file(bucket, chunk_file_path, dst_key)

            # Delete local chunk file
            os.remove(chunk_file_path)
    except Exception as e:
        print(f"Error in split_and_upload_csv: {e}")

def process_file(folder_prefix, file_content):
    src_key = file_content['Key']
    file_name = os.path.basename(src_key)
    local_file_path = os.path.join('local_directory', folder_prefix, file_name)

    # Create local folder if it doesn't exist
    local_folder = os.path.join('local_directory', folder_prefix)
    if not os.path.exists(local_folder):
        os.makedirs(local_folder)

    download_file(source_bucket, src_key, local_file_path)
    
    destination_folder_for_chunks = os.path.join(destination_folder, folder_prefix)
    split_and_upload_csv(local_file_path, source_bucket, destination_folder_for_chunks)
    
    # Delete original local file
    os.remove(local_file_path)

# Get the list of all folders and subfolders
paginator = s3_client.get_paginator('list_objects_v2')
page_iterator = paginator.paginate(Bucket=source_bucket, Prefix=source_folder, Delimiter='/')

for page in page_iterator:
    for content in page.get('CommonPrefixes', []):
        folder_prefix = content.get('Prefix')
        print(f"Processing folder: {folder_prefix}")

        folder_objects = s3_client.list_objects_v2(Bucket=source_bucket, Prefix=folder_prefix)
        
        futures = []
        for file_content in folder_objects.get('Contents', []):
            futures.append(executor.submit(process_file, folder_prefix, file_content))

        # Wait for all futures to complete
        for future in futures:
            future.result()
