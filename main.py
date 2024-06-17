import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from logger import get_logger
from exception import ConnectionError, RateLimitError, ContentPolicyViolationError, APIError, WordCountError, TextLengthError, PermissionError
from generator import revise_text
from text_to_speech import text_to_speech
from storage import upload_data_to_storage
from domain.readaloud_response import ReadAloudResponse
from domain.revise_response import ReviseResponse
from domain.readaloud_pubsub_message import ReadAloudPubSubMessage
from domain.revise_pubsub_message import RevisePubSubMessage
from pubsub import publish_to_read_aloud_usage_topic, publish_to_revise_usage_topic

logger = get_logger()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
chat_model_name_default = os.getenv("DEFAULT_CHAT_MODEL_NAME")
chat_model_name_premium = os.getenv("PREMIUM_CHAT_MODEL_NAME")


class ReviseParameters(BaseModel):
    uid: str
    text: str
    entry_id: str
    created_at: str
    is_billing: bool


class TextToSpeechParameters(BaseModel):
    uid: str
    text: str
    entry_id: str
    created_at: str
    is_billing: bool


@app.post("/generate/revise")
def generate_revised_entry(parameter: ReviseParameters):
    try:
        chat_model_name = chat_model_name_default
        if parameter.is_billing:
            chat_model_name = chat_model_name_premium
        result = revise_text(parameter.text, chat_model_name)
        response = ReviseResponse(revised_text=result.revised)
        created_at = parameter.created_at

        message = RevisePubSubMessage(
            uid=parameter.uid,
            text=parameter.text,
            revised_text=result.revised,
            entry_id=parameter.entry_id,
            created_at=created_at
        )
        publish_to_revise_usage_topic(data=message)

        return response

    except ConnectionError as e:
        logger.error(f"generate_revised_entry: {e}")
        raise HTTPException(
            status_code=504, detail=e.to_dict())

    except RateLimitError as e:
        logger.error(f"generate_revised_entry: {e}")
        raise HTTPException(
            status_code=503, detail=e.to_dict())

    except ContentPolicyViolationError as e:
        logger.error(f"generate_revised_entry: {e}")
        raise HTTPException(
            status_code=400, detail=e.to_dict())

    except APIError as e:
        logger.error(f"generate_revised_entry: {e}")
        raise HTTPException(
            status_code=500, detail=e.to_dict())

    except WordCountError as e:
        logger.error(f"generate_revised_entry: {e}")
        raise HTTPException(
            status_code=400, detail=e.to_dict())

    except TextLengthError as e:
        logger.error(f"generate_revised_entry: {e}")
        raise HTTPException(
            status_code=400, detail=e.to_dict())

    except Exception as e:
        logger.error(f"generate_revised_entry: {e}")
        raise HTTPException(
            status_code=500, detail={
                "message": f"{e}"
            })


@app.post(
    "/generate/readaloud",
)
def generate_readaloud(parameter: TextToSpeechParameters):
    try:
        if not parameter.is_billing:
            raise PermissionError()
        audio_content = text_to_speech(parameter.text)
        path = upload_data_to_storage(parameter.uid, audio_content)
        response = ReadAloudResponse(file_path=path)
        created_at = parameter.created_at

        message = ReadAloudPubSubMessage(
            uid=parameter.uid,
            text_to_speech=parameter.text,
            path=path,
            entry_id=parameter.entry_id,
            created_at=created_at
        )
        publish_to_read_aloud_usage_topic(data=message)

        return response

    except PermissionError as e:
        logger.error(f"generate_revised_entry: {e}")
        raise HTTPException(
            status_code=400, detail=e.to_dict())

    except Exception as e:
        logger.error(f"generate_voice: {e}")
        raise HTTPException(
            status_code=500, detail={
                "message": f"{e}"
            })
