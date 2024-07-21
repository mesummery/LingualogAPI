class ReadAloud:
    def __init__(
        self,
        audio: bytes,
        voice_type: str,
        voice_id: str
    ):
        self.audio = audio
        self.voice_type = voice_type
        self.voice_id = voice_id