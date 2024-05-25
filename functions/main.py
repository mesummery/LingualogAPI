# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn, options
from firebase_functions.params import IntParam, StringParam
from firebase_admin import initialize_app
from flask import jsonify
import os
from logger import get_logger
from generator import revise_text
from text_to_speech import text_to_speech
from exception import WordCountError, TextLengthError

initialize_app()
logger = get_logger()


@https_fn.on_call(
    cors=options.CorsOptions(
        # timeout_sec=5,
        cors_origins=[r"firebase\.com$"],
        # cors_methods=["post"],
    ),
)
def revise(req: https_fn.CallableRequest) -> any:
    text: str = req.data["text"]

    try:
        revised = revise_text(text)
        return revised.to_json()
    except WordCountError as e:
        logger.error(f"revise: {e}")
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.INVALID_ARGUMENT,
            message=f"{e.message}",
        )
    except TextLengthError as e:
        logger.error(f"revise: {e}")
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.INVALID_ARGUMENT,
            message=f"{e.message}",
        )
    except Exception as e:
        logger.error(f"revise: {e}")
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.UNAVAILABLE,
            message=f"{e}",
        )


@https_fn.on_call(
    cors=options.CorsOptions(
    #     # timeout_sec=5,
        cors_origins=[r"firebase\.com$"],
    #     cors_methods=["post"],
    ),
)
def readaloud(req: https_fn.CallableRequest) -> any:

    text: str = req.data["text"]

    # try:
    #     audio_content = text_to_speech(text)
    #     headers = {
    #         'Content-Type': 'audio/mpeg'
    #     }
    #     return https_fn.Response(audio_content, headers=headers)
    # except Exception as e:
    #     logger.error(f"readaloud: {e}")
    #     raise https_fn.HttpsError(
    #         code=https_fn.FunctionsErrorCode.UNAVAILABLE,
    #         message=f"{e}",
    #     )
