from dataclasses import dataclass, field

@dataclass
class TorrentItem:
    title: str | None = None
    desc: str | None = None
    guid: str | None = None
    comments: int | None = 0
    pub_date: str | None = None
    size: int | None = 0
    link: str | None = None
    categories: list[int] = field(default_factory=list)
    # torznab attributes
    infohash: str | None = None
    tvdb_id: int | None = None
    imdb_id: int | None = None
    magnet_url: str | None = None
    seeders: int | None = 0
    grabs: int | None = 0
    peers: int | None = 0
    min_ratio: float | None = 0
    min_seed_time: float | None = 0
    dl_volume_factor: float | None = 0
    ul_volume_factor: float | None = 0
    tags: list[str] = field(default_factory=list)
