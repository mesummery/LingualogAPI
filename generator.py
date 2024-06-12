import os
import json
import exception
from dotenv import load_dotenv
from openai import OpenAI, APIConnectionError, RateLimitError
from logger import get_logger
from domain.revised_entry import RevisedEntry
logger = get_logger()

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
chat_model_name = os.getenv("CHAT_MODEL_NAME")
min_words = int(os.getenv("MIN_WORDS"))
text_limit = int(os.getenv("REVISE_TEXT_LIMIT"))

client = OpenAI(api_key=openai_api_key)


def revise_text(text: str) -> RevisedEntry:
    if min_words > len(text.split()):
        raise exception.WordCountError(message="The text contains too few words.")

    if len(text) > text_limit:
        raise exception.TextLengthError(message="The text is too long.")

    prompt = f"""
    "{text}"
    ---
    I wrote the above diary in English. Please return the corrected text with any grammatical mistakes or awkward expressions revised.
    """
    revised = __generate_revised_text(prompt)
    return revised


def __generate_revised_text(prompt: str) -> RevisedEntry:
    logger.info(f"Generating text with {chat_model_name}")
    logger.info(f"Prompt {prompt}")
    try:
        response = client.chat.completions.create(
            model=chat_model_name,
            messages=[
                {"role": "system", "content": prompt},
            ],
            functions=[
                {"name": "set_definition", "parameters": schema}
            ],
            function_call={"name": "set_definition"},
            # response_format={"type": "json_object"}, # FIXME: use gpt-4-1106-previewgpt-3.5-turbo-1106
        )
        answer = response.choices[0].message.function_call.arguments
        logger.info(answer)
        dict = json.loads(answer)
        logger.info(f"Answer: {dict}")
        entry = RevisedEntry.from_json(dict)
        return entry
    except APIConnectionError as e:
        raise exception.ConnectionError(e)
    except RateLimitError as e:
        raise exception.RateLimitError(e)
    except Exception as e:
        raise exception.APIError(e)


schema = {
    "title": "英文添削スキーマ",
    "type": "object",
    "properties": {
        "revised": {
            "type": "string",
            "description": "添削済の英文"
        },
    },
    "required": [
        "revised",
    ]
}
