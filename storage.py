import os
from dotenv import load_dotenv
import time
from logger import get_logger
from google.cloud import storage

logger = get_logger()

load_dotenv()
# creadential = SecretParam("GOOGLE_APPLICATION_CREDENTIALS").value
bucket_name = os.getenv("STORAGE_BUCKET")
blob_prefix = os.getenv("DESTINATION_BLOB_PREFIX")

storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)


def upload_data_to_storage(uuid: str, data: bytes) -> str:
    current_unix_time = int(time.time())
    destination_blob_name = f"{blob_prefix}/{uuid}/{current_unix_time}.mp3"
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(data, content_type="audio/mpeg")
    logger.info(f"File uploaded: {destination_blob_name}")
    return destination_blob_name
