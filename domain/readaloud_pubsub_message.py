class ReadAloudPubSubMessage:
    def __init__(
        self: int,
        uid: str,
        text_to_speech: str,
    ):
        self.uid = uid
        self.text_to_speech = text_to_speech

    def to_dict(self) -> dict[str, any]:
        return {
            "uid": self.uid,
            "text_to_speech": self.text_to_speech,
        }
