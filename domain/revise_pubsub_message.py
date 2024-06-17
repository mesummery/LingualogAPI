class RevisePubSubMessage:
    def __init__(
        self,
        uid: str,
        text: str,
        revised_text: str,
        entry_id: str,
        created_at: str
    ):
        self.uid = uid
        self.text = text
        self.revised_text = revised_text
        self.entry_id = entry_id
        self.created_at = created_at

    def to_dict(self) -> dict[str, any]:
        return {
            "uid": self.uid,
            "text": self.text,
            "revised_text": self.revised_text,
            "entry_id": self.entry_id,
            "created_at": self.created_at,
        }
