import configparser
import json
from datetime import datetime
from time import sleep

from google.cloud import storage
from google.oauth2 import service_account
from kafka import KafkaConsumer


parser = configparser.ConfigParser()
parser.read("upstash.conf")

upstash_bootstrap_servers = parser.get("config", "upstash_bootstrap_servers")
upstash_username = parser.get("config", "upstash_username")
upstash_password = parser.get("config", "upstash_password")

GCP_PROJECT_ID = "turing-chess-434208-a6"
BUCKET_NAME = "deb4-bootcamp-014"
BUSINESS_DOMAIN = "networkrail"
DESTINATION_FOLDER = f"{BUSINESS_DOMAIN}/raw"
KEYFILE_PATH = "/workspaces/data-engineering-bootcamp/00-bootcamp-project/deb4-uploading-files-to-gcs.json"
CONSUMER_GROUP = "deb4-bootcamp-014"

consumer = KafkaConsumer(
    "networkrail-train-movements",
    bootstrap_servers=upstash_bootstrap_servers,
    sasl_mechanism="SCRAM-SHA-256",
    security_protocol="SASL_SSL",
    sasl_plain_username=upstash_username,
    sasl_plain_password=upstash_password,
    group_id=CONSUMER_GROUP,
    auto_offset_reset="earliest",
)

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    # keyfile = os.environ.get("KEYFILE_PATH")
    keyfile = KEYFILE_PATH
    service_account_info = json.load(open(keyfile))
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
    project_id = GCP_PROJECT_ID

    storage_client = storage.Client(
        project=project_id,
        credentials=credentials,
    )
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

try:
    for message in consumer:
        try:
            data = json.loads(message.value.decode("utf-8"))
            print(data)

            train_id = data["train_id"]
            now = int(datetime.now().timestamp())
            file_name = f"{train_id}-{now}.json"
            source_file_name = f"data/{file_name}"
            with open(source_file_name, "w") as f:
                json.dump(data, f)

            upload_to_gcs(
                bucket_name=BUCKET_NAME,
                source_file_name=source_file_name,
                destination_blob_name=f"{DESTINATION_FOLDER}/{file_name}",
            )

            sleep(3)
        except json.decoder.JSONDecodeError:
            pass

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
