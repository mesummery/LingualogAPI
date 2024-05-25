class RevisedEntry:
    def __init__(
        self,
        revised: str,
    ):
        self.revised = revised

    @classmethod
    def from_json(cls, json_data):
        revised = json_data['revised']

        return cls(
            revised,
        )
