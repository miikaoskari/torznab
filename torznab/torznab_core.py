# Contains functions/classes for making requests to Torznab servers, handling responses, and parsing XML/JSON data.
import requests
from lxml import objectify

class Torznab:
    def __init__(self, url, api_key=None):
        self.url = url
        self.api_key = api_key

    def caps(self):
        return self._request("?t=caps")

    def search(self):
        return self._request("?t=search")

    def tv_search(self):
        return self._request("?t=tvsearch")

    def movie(self):
        return self._request("?t=movie")

    def music(self):
        return self._request("?t=music")

    def book(self):
        return self._request("?t=book")

    def _request(self, params):
        if self.api_key is not None:
            params += f"&apikey={self.api_key}"
        response = requests.get(self.url + params)
        xml_content = response.content
        print(xml_content)
        return objectify.fromstring(xml_content)
    
if __name__ == "__main__":
    import json
    with open("key.json", "r") as f:
        api = json.load(f)
    torznab = Torznab(url=api["url"], api_key=api["key"])
    result = torznab.caps()
    print(result)
    
