import os
# import io
import emoji
from dotenv import load_dotenv
from google.cloud import texttospeech
from logger import get_logger
from domain.readaloud import ReadAloud
# from openai import OpenAI

logger = get_logger()
load_dotenv()
# openai_api_key = os.getenv("OPENAI_API_KEY")
# openAIClient = OpenAI(api_key=openai_api_key)
standard_voice_id = os.getenv("STANDARD_VOICE_NAME")
premium_voice_id = os.getenv("PREMIUM_VOICE_NAME")

client = texttospeech.TextToSpeechClient()


def _get_voice_name(voice_id: str, voice_type: str) -> str:
    logger.debug(f"voice_id {voice_id}")
    logger.debug(f"voice_type {voice_type}")

    # API仕様が変わった時に前のアプリバージョンをサポートする
    if voice_type == "premium":
        if voice_id == "":
            return premium_voice_id
        else:
            return voice_id
    return standard_voice_id


def text_to_speech(text: str, voice_id: str, voice_type: str) -> ReadAloud:

    # if voice_type != "":
    #     response = openAIClient.audio.speech.create(
    #         model="tts-1",
    #         voice="alloy",
    #         response_format="mp3",
    #         input=text,
    #     )
    #     return response.content

    replaced_text = emoji.replace_emoji(text, replace='.')
    synthesis_input = texttospeech.SynthesisInput(text=replaced_text)
    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice_name = _get_voice_name(voice_id, voice_type)
    logger.info(f'voice_name: {voice_name}')
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        # ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        name=voice_name
    )
    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return ReadAloud(
        audio=response.audio_content,
        voice_type=voice_type,
        voice_id=voice_name
    )
