from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from logger import get_logger
from exception import ConnectionError, RateLimitError, ContentPolicyViolationError, APIError
from functions.generator import revise
from text_to_speech import text_to_speech

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
    draft: str


class TextToSpeechParameters(BaseModel):
    text: str


@app.post("/generate/revise")
def generate_revised_entry(parameter: ReviseParameters):
    try:
        revised = revise(parameter.draft)
        return revised

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

    except Exception as e:
        logger.error(f"generate_revised_entry: {e}")
        raise HTTPException(
            status_code=500, detail={
                "message": f"{e}"
            })


@app.post(
    "/generate/voice",
    response_class=Response
)
def generate_voice(parameter: TextToSpeechParameters):
    try:
        audio_content = text_to_speech(parameter.text)
        return Response(audio_content, media_type='audio/mpeg')

    except Exception as e:
        logger.error(f"generate_voice: {e}")
        raise HTTPException(
            status_code=500, detail={
                "message": f"{e}"
            })
