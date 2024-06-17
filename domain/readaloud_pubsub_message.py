class ReadAloudPubSubMessage:
    def __init__(
        self,
        uid: str,
        text_to_speech: str,
        path: str,
        entry_id: str,
        created_at: str
    ):
        self.uid = uid
        self.text_to_speech = text_to_speech
        self.path = path
        self.entry_id = entry_id
        self.created_at = created_at

    def to_dict(self) -> dict[str, any]:
        return {
            "uid": self.uid,
            "text_to_speech": self.text_to_speech,
            "path": self.path,
            "entry_id": self.entry_id,
            "created_at": self.created_at,
        }
