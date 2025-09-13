from dataclasses import dataclass

@dataclass
class TorrentItem:
    title: str | None = None
    guid: str | None = None
    link: str | None = None
    size: str | None = None
    categories: list[str] | None = None
    attrs: dict[str, str] | None = None
