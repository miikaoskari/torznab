from urllib.parse import urlparse


class ValidationError(Exception):
    pass


def is_url(url: str) -> bool:
    result = urlparse(url)
    if not all([result.scheme, result.netloc]):
        raise ValidationError(f"Invalid URL: '{url}'")
    return True
