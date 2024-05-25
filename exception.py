class TextLengthError(Exception):

    def __init__(self, message: str):
        self.code = "text_length"
        self.message = message

    def to_dict(self) -> dict[str, any]:
        return {
            "code": self.code,
            "message": self.message
        }


class WordCountError(Exception):

    def __init__(self, message: str):
        self.code = "word_count"
        self.message = message

    def to_dict(self) -> dict[str, any]:
        return {
            "code": self.code,
            "message": self.message
        }


class APIError(Exception):

    def __init__(self, e):
        self.e = e
        self.code = "exception"
        self.message = f"Failed to generate by OpenAI API: {e}"
        super().__init__(self.message)

    def to_dict(self) -> dict[str, any]:
        return {
            "code": self.code,
            "message": self.message
        }


class ContentPolicyViolationError(APIError):

    def __init__(self, e):
        self.e = e
        self.code = "content_policy_violation"
        self.message = f"The request was rejected as a result of OpenAI safety system: {e}"


class RateLimitError(APIError):

    def __init__(self, e):
        self.e = e
        self.code = "rate_limit"
        self.message = f"OpenAI API request exceeded rate limit: {e}"


class ConnectionError(APIError):

    def __init__(self, e):
        self.e = e
        self.code = "connection"
        self.message = f"Failed to connect to OpenAI API: {e}"


class ValidationError(APIError):

    def __init__(self, e, message: str):
        self.e = e
        self.code = "validation"
        self.message = f"{message}: {e}"


class InputWordError(APIError):

    def __init__(self, message: str):
        self.code = "ng_word"
        self.message = message
