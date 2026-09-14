import xml.etree.ElementTree as ET

import requests

from .exceptions import TorznabConnectionError, TorznabParseError
from .parser import parse_capabilities, parse_torznab
from .types import Capabilities, TorrentItem
from .validators import validate_url

DEFAULT_TIMEOUT = 30


class Torznab:
    def __init__(
        self, api_key: str | None = None, timeout: float = DEFAULT_TIMEOUT
    ) -> None:
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()

    def _search(self, url: str, full_query: dict, timeout: float) -> str:
        resp = self.session.get(url, params=full_query, timeout=timeout)
        resp.raise_for_status()
        return resp.text

    def search_torrent(
        self,
        query: str,
        url: str,
        api_key: str | None = None,
        timeout: float | None = None,
    ) -> list[TorrentItem]:
        validate_url(url)
        key = api_key if api_key is not None else self.api_key
        full_query = {
            "t": "search",
            "q": query,
            **({"apikey": key} if key else {}),
        }
        resolved_timeout = timeout if timeout is not None else self.timeout
        try:
            return parse_torznab(self._search(url, full_query, resolved_timeout))
        except requests.RequestException as e:
            raise TorznabConnectionError(str(e)) from e
        except ET.ParseError as e:
            raise TorznabParseError(str(e)) from e

    def get_capabilities(
        self,
        url: str,
        api_key: str | None = None,
        timeout: float | None = None,
    ) -> Capabilities:
        validate_url(url)
        key = api_key if api_key is not None else self.api_key
        full_query = {
            "t": "caps",
            **({"apikey": key} if key else {}),
        }
        resolved_timeout = timeout if timeout is not None else self.timeout
        try:
            return parse_capabilities(self._search(url, full_query, resolved_timeout))
        except requests.RequestException as e:
            raise TorznabConnectionError(str(e)) from e
        except ET.ParseError as e:
            raise TorznabParseError(str(e)) from e
