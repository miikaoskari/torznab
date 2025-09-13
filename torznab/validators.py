from urllib.parse import urlparse

class ValidationError(Exception):
    pass

def is_url(url):
    result = urlparse(url)
    if not all([result.scheme, result.netloc]):
        raise ValidationError("Invalid URL")
