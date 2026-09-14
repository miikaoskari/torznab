from urllib.parse import urlparse

from .exceptions import TorznabValidationError


def is_url(url: str) -> bool:
    result = urlparse(url)
    if not all([result.scheme, result.netloc]):
        raise TorznabValidationError(f"Invalid URL: '{url}'")
    return True
