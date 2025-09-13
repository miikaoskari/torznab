import xml.etree.ElementTree as ET
from .types import TorrentItem

ns = {
    "torznab": "http://torznab.com/schemas/2015/feed"
}

def parse_torznab(xml_string: str):
    root = ET.fromstring(xml_string)
    items = []
    for item in root.findall('.//item'):
        torrent = TorrentItem(
            title=item.findtext("title"),
            guid=item.findtext("guid"),
            link=item.findtext("link"),
            size=item.findtext("size"),
        )
        items.append(torrent)
    return items