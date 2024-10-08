class ReadAloudPubSubMessage:
    def __init__(
        self,
        uid: str,
        text_to_speech: str,
        voice_id: str,
        voice_type: str,
        path: str,
        entry_id: str,
        created_at: str,
        tid: str | None,
        original_tid: str | None,
        expiration_date: str | None,
    ):
        self.uid = uid
        self.tid = tid
        self.original_tid = original_tid
        self.text_to_speech = text_to_speech
        self.voice_id = voice_id
        self.voice_type = voice_type
        self.path = path
        self.entry_id = entry_id
        self.created_at = created_at
        self.expiration_date = expiration_date

    def to_dict(self) -> dict[str, any]:
        dictionary = {
            "uid": self.uid,
            "text_to_speech": self.text_to_speech,
            "voice_id": self.voice_id,
            "voice_type": self.voice_type,
            "path": self.path,
            "entry_id": self.entry_id,
            "created_at": self.created_at,
        }

        if self.tid is not None and self.original_tid is not None and self.expiration_date is not None:
            dictionary["tid"] = self.tid
            dictionary["original_tid"] = self.original_tid
            dictionary["expiration_date"] = self.expiration_date

        return dictionary
