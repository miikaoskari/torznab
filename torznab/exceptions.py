class TorznabException(Exception):
    pass


class TorznabAPIError(TorznabException):
    def __init__(self, code: int | None, description: str | None) -> None:
        self.code = code
        self.description = description
        super().__init__(f"Torznab API error {code}: {description}")


class TorznabValidationError(TorznabException):
    pass


class TorznabConnectionError(TorznabException):
    pass


class TorznabParseError(TorznabException):
    pass
