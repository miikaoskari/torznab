from dataclasses import dataclass

@dataclass
class TorrentItem:
    title: str | None = None
    desc: str | None = None
    guid: str | None = None
    comments: str | None = None
    pub_date: str | None = None
    size: str | None = None
    link: str | None = None
    size: str | None = None
    categories: list[str | None] | None = None
    attrs: dict[str, list[str]] | None = None
