import time
import firebase_admin
from firebase_admin import storage
from firebase_functions.params import StringParam, SecretParam
from logger import get_logger

logger = get_logger()

# creadential = SecretParam("GOOGLE_APPLICATION_CREDENTIALS").value
bucket_name = StringParam("STORAGE_BUCKET").value
blob_prefix = StringParam("DESTINATION_BLOB_PREFIX").value

firebase_admin.initialize_app()

bucket = storage.bucket()


def upload_data_to_storage(uuid: str, data: bytes) -> str:
    current_unix_time = int(time.time())
    destination_blob_name = f"{blob_prefix}/{uuid}/{current_unix_time}.jpg"
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(data, content_type="audio/mpeg")
    logger.info(f"File uploaded: {destination_blob_name}")
    return destination_blob_name
