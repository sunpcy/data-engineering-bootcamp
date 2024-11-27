import json

import os

from google.cloud import storage
from google.oauth2 import service_account


DATA_FOLDER = "data"
BUSINESS_DOMAIN = "greenery"
project_id = "turing-chess-434208-a6"
location = "asia-southeast1"
bucket_name = "deb4-bootcamp-014"
# data = "addresses"

# Prepare and Load Credentials to Connect to GCP Services
keyfile_gcs = "deb4-uploading-files-to-gcs.json"
service_account_info_gcs = json.load(open(keyfile_gcs))
credentials_gcs = service_account.Credentials.from_service_account_info(
    service_account_info_gcs
)

# Load data from Local to GCS
storage_client = storage.Client(
    project=project_id,
    credentials=credentials_gcs,
)
bucket = storage_client.bucket(bucket_name)

'''
file_path = f"{DATA_FOLDER}/{data}.csv"
destination_blob_name = f"raw/{BUSINESS_DOMAIN}/{data}/{data}.csv"

# YOUR CODE HERE TO LOAD DATA TO GCS

blob = bucket.blob(destination_blob_name)
blob.upload_from_filename(file_path)
'''

# Loop through all files in the folder
for file_name in os.listdir(DATA_FOLDER):
    if os.path.isfile(os.path.join(DATA_FOLDER, file_name)) and file_name.endswith('.csv'):
        # Remove the file extension (.csv)
        data = os.path.splitext(file_name)[0]
        
        # Build file paths
        file_path = f"{DATA_FOLDER}/{data}.csv"
        destination_blob_name = f"raw/{BUSINESS_DOMAIN}/{data}/{data}.csv"
        
        # YOUR CODE HERE TO LOAD DATA TO GCS
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(file_path)

        print(f"Uploaded {file_path} to {destination_blob_name}")