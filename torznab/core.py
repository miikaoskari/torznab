import requests

from .validators import is_url
from .parser import parse_torznab

class Torznab:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def search_torrent(self, query: str, url: str):
        try:
            is_url(url)
            querystring = {"apikey":self.api_key,"t":"search","q":query}
            response = requests.get(url, params=querystring)
            return parse_torznab(response.text)
        except Exception as e:
            print(e)
