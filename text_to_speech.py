import emoji
from google.cloud import texttospeech
from logger import get_logger

logger = get_logger()

client = texttospeech.TextToSpeechClient()

def text_to_speech(text: str):
    replaced_text = emoji.replace_emoji(text, replace='.')
    synthesis_input = texttospeech.SynthesisInput(text=replaced_text)
    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", 
        # ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        name="en-US-Wavenet-D"
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
    return response.audio_content
