import json
import exception
from firebase_functions.params import IntParam, StringParam, SecretParam
from openai import OpenAI, APIConnectionError, RateLimitError
# from dotenv import load_dotenv
from logger import get_logger
from domain.revised_entry import RevisedEntry
logger = get_logger()

openai_api_key = SecretParam("OPENAI_API_KEY").value
chat_model_name = StringParam("CHAT_MODEL_NAME").value
min_words = IntParam("MIN_WORDS").value
text_limit = IntParam("REVISE_TEXT_LIMIT").value

client = OpenAI(api_key=openai_api_key)


def __is_valid_word_count(text: str) -> bool:
    if min_words > len(text.split()):
        logger.info(f"{text} is NG.")
        return False
    else:
        logger.info(f"{text} is OK.")
        return True


def revise_text(text: str) -> RevisedEntry:
    if min_words > len(text.split()):
        raise exception.WordCountError(message="The text contains too few words.")

    if len(text) > text_limit:
        raise exception.WordCountError(message="The text is too long.")

    prompt = f"""
    {text}
    ---
    英語の日記を書きました。文法の間違いや不自然な表現を添削をした文章を返してください。
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
