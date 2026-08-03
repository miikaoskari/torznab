from dataclasses import dataclass, field


@dataclass(slots=True)
class MediaInfo:
    genre: str | None = None
    video: str | None = None
    resolution: str | None = None
    framerate: str | None = None
    subs: str | None = None


@dataclass(slots=True)
class TVInfo:
    season: int | None = None
    episode: int | None = None
    rage_id: int | None = None
    tv_title: str | None = None
    airdate: str | None = None
    tvdb_id: int | None = None
    tvmaze_id: int | None = None


@dataclass(slots=True)
class MovieInfo:
    imdb_id: str | None = None
    imdb_score: str | None = None
    imdb_title: str | None = None
    imdb_tagline: str | None = None
    imdb_plot: str | None = None
    imdb_year: int | None = None
    imdb_director: str | None = None
    imdb_actors: str | None = None


@dataclass(slots=True)
class AudioInfo:
    audio: str | None = None
    language: str | None = None


@dataclass(slots=True)
class MusicInfo:
    artist: str | None = None
    album: str | None = None
    publisher: str | None = None
    tracks: str | None = None


@dataclass(slots=True)
class BookInfo:
    book_title: str | None = None
    publish_date: str | None = None
    author: str | None = None
    pages: int | None = None


@dataclass(slots=True)
class TorrentItem:
    title: str | None = None
    size: int | None = None
    categories: list[int] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    guid: str | None = None
    files: list[int] = field(default_factory=list)
    poster: str | None = None
    group: str | None = None
    team: str | None = None
    grabs: int | None = None
    seeders: int | None = None
    leechers: int | None = None
    peers: int | None = None
    infohash: str | None = None
    magnet_url: str | None = None
    seed_type: str | None = None
    min_ratio: float | None = None
    min_seed_time: float | None = None
    dl_volume_factor: float | None = 1.0
    ul_volume_factor: float | None = 1.0
    password: int | None = None
    comments: int | None = None
    nfo: int | None = None
    info: str | None = None
    year: int | None = None
    cover_url: str | None = None
    backdrop_url: str | None = None
    desc: str | None = None
    pub_date: str | None = None
    link: str | None = None

    media_info: MediaInfo | None = None
    tv_info: TVInfo | None = None
    movie_info: MovieInfo | None = None
    audio_info: AudioInfo | None = None
    music_info: MusicInfo | None = None
    book_info: BookInfo | None = None

    @property
    def is_freeleech(self) -> bool:
        return self.dl_volume_factor == 0.0
