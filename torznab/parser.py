import xml.etree.ElementTree as ET
from .types import TorrentItem

ns = {
    "torznab": "http://torznab.com/schemas/2015/feed"
}

def parse_torznab(xml_string: str) -> list[TorrentItem]:
    root = ET.fromstring(xml_string)
    items = []
    for item in root.findall(".//item"):
        # these attributes may occur multiple times
        categories = [int(cat.text) for cat in item.findall("category") if cat.text and cat.text.isdigit()]

        tags = []
        for attr in item.findall("torznab:attr", ns):
            if attr.get("name") == "tag" and (val := attr.get("value")):
                tags.append(val)

        torznab_attrs = {}
        for attr in item.findall("torznab:attr", ns):
            torznab_attrs[attr.get("name")] = attr.get("value")

        torrent = TorrentItem(
            title=item.findtext("title"),
            desc=item.findtext("description"),
            guid=item.findtext("guid"),
            comments=int(item.findtext("comments", 0)),
            pub_date=item.findtext("pubDate"),
            size=int(item.findtext("size", 0)),
            link=item.findtext("link"),
            categories=categories,
            tags=tags,
            tvdb_id=int(torznab_attrs.get("tvdbid", 0)),
            imdb_id=int(torznab_attrs.get("imdbid", 0)),
            magnet_url=torznab_attrs.get("magneturl"),
            seeders=int(torznab_attrs.get("seeders", 0)),
            grabs=int(torznab_attrs.get("grabs", 0)),
            peers=int(torznab_attrs.get("peers", 0)),
            infohash=torznab_attrs.get("infohash"),
            dl_volume_factor=float(torznab_attrs.get("downloadvolumefactor", 0)),
            ul_volume_factor=float(torznab_attrs.get("uploadvolumefactor", 0)),
            min_ratio=float(torznab_attrs.get("minimumratio", 0))
        )
        items.append(torrent)
    return items
