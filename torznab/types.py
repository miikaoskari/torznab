from dataclasses import dataclass

@dataclass
class TorrentItem:
    title: str | None = None
    desc: str | None = None
    guid: str | None = None
    comments: int | None = None
    pub_date: str | None = None
    size: int | None = None
    link: str | None = None
    categories: list[int] | None = None
    # torznab attributes
    infohash: str | None = None
    tvdb_id: int | None = None
    imdb_id: int | None = None
    magnet_url: str | None = None
    seeders: int | None = None
    grabs: int | None = None
    peers: int | None = None
    min_ratio: float | None = None
    min_seed_time: float | None = None
    dl_volume_factor: float | None = None
    ul_volume_factor: float | None = None
    tags: list[str] | None = None
