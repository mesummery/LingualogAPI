from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from logger import get_logger
from exception import ConnectionError, RateLimitError, ContentPolicyViolationError, APIError, WordCountError, TextLengthError
from generator import revise_text
from text_to_speech import text_to_speech
from storage import upload_data_to_storage
from domain.readaloud_response import ReadAloudResponse
from domain.revise_response import ReviseResponse

logger = get_logger()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ReviseParameters(BaseModel):
    text: str


class TextToSpeechParameters(BaseModel):
    text: str
    uuid: str


@app.post("/generate/revise")
def generate_revised_entry(parameter: ReviseParameters):
    try:
        result = revise_text(parameter.text)
        response = ReviseResponse(revised_text=result.revised)
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
        audio_content = text_to_speech(parameter.text)
        path = upload_data_to_storage(parameter.uuid, audio_content)
        response = ReadAloudResponse(file_path=path)
        return response

    except Exception as e:
        logger.error(f"generate_voice: {e}")
        raise HTTPException(
            status_code=500, detail={
                "message": f"{e}"
            })
