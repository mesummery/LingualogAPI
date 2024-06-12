class RevisePubSubMessage:
    def __init__(
        self: int,
        uid: str,
        text: str,
        revised_text: str
    ):
        self.uid = uid
        self.text = text
        self.revised_text = revised_text

    def to_dict(self) -> dict[str, any]:
        return {
            "uid": self.uid,
            "text": self.text,
            "revised_text": self.revised_text
        }
