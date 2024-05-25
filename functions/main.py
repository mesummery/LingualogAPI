# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

import firebase_admin
from firebase_functions import https_fn, options
from logger import get_logger
from generator import revise_text
from text_to_speech import text_to_speech
from storage import upload_data_to_storage
from exception import WordCountError, TextLengthError

# firebase_admin.initialize_app()
logger = get_logger()

@https_fn.on_call(
    cors=options.CorsOptions(
        # timeout_sec=5,
        cors_origins=[r"firebase\.com$"],
        # cors_methods=["post"],
    ),
)
def revise(req: https_fn.CallableRequest) -> any:

    try:
        text: str = req.data["text"]
        result = revise_text(text)
        return {
            "revised_text": result.revised
        }
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

    try:
        text: str = req.data["text"]
        uid = req.auth.uid
        audio_content = text_to_speech(text)
        url = upload_data_to_storage(uid, audio_content)
        return {
            "readaloud_url": url
        }
    
    except Exception as e:
        logger.error(f"readaloud: {e}")
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.UNAVAILABLE,
            message=f"{e}",
        )
