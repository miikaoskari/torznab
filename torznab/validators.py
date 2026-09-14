from urllib.parse import urlparse

from .exceptions import TorznabValidationError


def validate_url(url: str) -> None:
    result = urlparse(url)
    if not all([result.scheme, result.netloc]):
        raise TorznabValidationError(f"Invalid URL: '{url}'")
