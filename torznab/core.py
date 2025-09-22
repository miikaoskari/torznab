import requests

from .validators import is_url
from .parser import parse_torznab
from .types import TorrentItem
from .exceptions import TorznabException

class Torznab:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.session = requests.Session()

    def _search(self, url: str, full_query: dict) -> str:
        resp = self.session.get(url, params=full_query)
        resp.raise_for_status()
        return resp.text

    def search_torrent(self, query: str, url: str) -> list[TorrentItem]:
        try:
            is_url(url)
            full_query = {
                "t":"search",
                "q":query,
                **({"apikey": self.api_key} if self.api_key else {})
            }
            return parse_torznab(self._search(url, full_query))
        except Exception as e:
            raise TorznabException from e
