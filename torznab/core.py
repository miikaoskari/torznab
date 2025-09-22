import requests

from .validators import is_url
from .parser import parse_torznab
from .types import TorrentItem

class Torznab:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def _search(self, url: str, full_query: dict) -> str:
        return requests.get(url, params=full_query).text

    def search_torrent(self, query: str, url: str) -> list[TorrentItem] | None:
        try:
            is_url(url)
            full_query = {
                "t":"search",
                "q":query,
                **({"apikey": self.api_key} if self.api_key else {})
            }
            return parse_torznab(self._search(url, full_query))
        except Exception as e:
            print(e)

    def search_multiple_torrents(self, query: str, urls: dict) -> list[TorrentItem] | None:
        try:
            for url in urls:
                self.search_torrent(query, url)
        except Exception as e:
            print(e)
