import os
import json
from google.cloud import pubsub_v1
from domain.revise_pubsub_message import RevisePubSubMessage
from domain.readaloud_pubsub_message import ReadAloudPubSubMessage
from dotenv import load_dotenv
from logger import get_logger
logger = get_logger()

load_dotenv()
project_id = os.getenv("PROJECT_ID")
read_aloud_usage_topic = os.getenv("READ_ALOUD_USAGE_PUBSUB_TOPIC")
revise_usage_topic = os.getenv("REVISE_USAGE_PUBSUB_TOPIC")

publisher = pubsub_v1.PublisherClient()


def publish_to_revise_usage_topic(data: RevisePubSubMessage):
    try:
        logger.info( os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
        topic_path = publisher.topic_path(project_id, revise_usage_topic)
        message = json.dumps(
            {
                "data": data.to_dict(),
            }
        )
        message_bytes = message.encode("utf-8")
        future = publisher.publish(
            topic_path, data=message_bytes)
        future.result()

    except Exception as e:
        logger.error(f"failed to publish topic {revise_usage_topic} : {e}")


def publish_to_read_aloud_usage_topic(data: ReadAloudPubSubMessage):
    try:
        topic_path = publisher.topic_path(project_id, read_aloud_usage_topic)
        message = json.dumps(
            {
                "data": data.to_dict(),
            }
        )
        message_bytes = message.encode("utf-8")
        future = publisher.publish(
            topic_path, data=message_bytes)
        future.result()

    except Exception as e:
        logger.error(f"failed to publish topic {read_aloud_usage_topic} : {e}")
