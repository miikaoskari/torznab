import xml.etree.ElementTree as ET

from .exceptions import TorznabAPIError
from .types import (
    AudioInfo,
    BookInfo,
    Capabilities,
    Category,
    Genre,
    Limits,
    MediaInfo,
    MovieInfo,
    MusicInfo,
    Registration,
    Searching,
    SearchMode,
    Server,
    SubCategory,
    Tag,
    TorrentItem,
    TVInfo,
)

ns = {"torznab": "http://torznab.com/schemas/2015/feed"}


def _parse_int(val: str | None) -> int | None:
    if val is None:
        return None
    try:
        return int(val)
    except ValueError:
        return None


def _parse_float(val: str | None, default: float | None = None) -> float | None:
    if val is None:
        return default
    try:
        return float(val)
    except ValueError:
        return default


def _parse_bool(val: str | None) -> bool | None:
    if val is None:
        return None
    return val.strip().lower() == "yes"


def _check_for_error(root: ET.Element) -> None:
    if root.tag == "error":
        raise TorznabAPIError(
            code=_parse_int(root.get("code")),
            description=root.get("description"),
        )


def _parse_media_info(attrs: dict[str, str]) -> MediaInfo | None:
    genre = attrs.get("genre")
    video = attrs.get("video")
    resolution = attrs.get("resolution")
    framerate = attrs.get("framerate")
    subs = attrs.get("subs")

    if any(field is not None for field in (genre, video, resolution, framerate, subs)):
        return MediaInfo(
            genre=genre,
            video=video,
            resolution=resolution,
            framerate=framerate,
            subs=subs,
        )
    return None


def _parse_tv_info(attrs: dict[str, str]) -> TVInfo | None:
    season = _parse_int(attrs.get("season"))
    episode = _parse_int(attrs.get("episode"))
    rage_id = _parse_int(attrs.get("rageid"))
    tv_title = attrs.get("tvtitle")
    airdate = attrs.get("tvairdate")
    tvdb_id = _parse_int(attrs.get("tvdbid"))
    tvmaze_id = _parse_int(attrs.get("tvmazeid"))

    if any(
        field is not None
        for field in (season, episode, rage_id, tv_title, airdate, tvdb_id, tvmaze_id)
    ):
        return TVInfo(
            season=season,
            episode=episode,
            rage_id=rage_id,
            tv_title=tv_title,
            airdate=airdate,
            tvdb_id=tvdb_id,
            tvmaze_id=tvmaze_id,
        )
    return None


def _parse_movie_info(attrs: dict[str, str]) -> MovieInfo | None:
    imdb_id = attrs.get("imdb")
    imdb_score = attrs.get("imdbscore")
    imdb_title = attrs.get("imdbtitle")
    imdb_tagline = attrs.get("imdbtagline")
    imdb_plot = attrs.get("imdbplot")
    imdb_year = _parse_int(attrs.get("imdbyear"))
    imdb_director = attrs.get("imdbdirector")
    imdb_actors = attrs.get("imdbactors")

    if any(
        field is not None
        for field in (
            imdb_id,
            imdb_score,
            imdb_title,
            imdb_tagline,
            imdb_plot,
            imdb_year,
            imdb_director,
            imdb_actors,
        )
    ):
        return MovieInfo(
            imdb_id=imdb_id,
            imdb_score=imdb_score,
            imdb_title=imdb_title,
            imdb_tagline=imdb_tagline,
            imdb_plot=imdb_plot,
            imdb_year=imdb_year,
            imdb_director=imdb_director,
            imdb_actors=imdb_actors,
        )
    return None


def _parse_audio_info(attrs: dict[str, str]) -> AudioInfo | None:
    audio = attrs.get("audio")
    language = attrs.get("language")

    if any(field is not None for field in (audio, language)):
        return AudioInfo(
            audio=audio,
            language=language,
        )
    return None


def _parse_music_info(attrs: dict[str, str]) -> MusicInfo | None:
    artist = attrs.get("artist")
    album = attrs.get("album")
    publisher = attrs.get("publisher")
    tracks = attrs.get("tracks")

    if any(field is not None for field in (artist, album, publisher, tracks)):
        return MusicInfo(
            artist=artist,
            album=album,
            publisher=publisher,
            tracks=tracks,
        )
    return None


def _parse_book_info(attrs: dict[str, str]) -> BookInfo | None:
    book_title = attrs.get("booktitle")
    publish_date = attrs.get("publishdate")
    author = attrs.get("author")
    pages = _parse_int(attrs.get("pages"))

    if any(field is not None for field in (book_title, publish_date, author, pages)):
        return BookInfo(
            book_title=book_title,
            publish_date=publish_date,
            author=author,
            pages=pages,
        )
    return None


def parse_torznab(xml_string: str) -> list[TorrentItem]:
    root = ET.fromstring(xml_string)
    _check_for_error(root)
    items = []
    for item in root.findall(".//item"):
        categories = [
            int(cat.text)
            for cat in item.findall("category")
            if cat.text and cat.text.isdigit()
        ]

        tags = []
        torznab_attrs = {}
        for attr in item.findall("torznab:attr", ns):
            torznab_attrs[attr.get("name")] = attr.get("value")
            if attr.get("name") == "tag" and (val := attr.get("value")):
                tags.append(val)

        files_val = _parse_int(torznab_attrs.get("files"))
        files = [files_val] if files_val is not None else []

        torrent = TorrentItem(
            title=item.findtext("title"),
            desc=item.findtext("description"),
            guid=item.findtext("guid"),
            comments=_parse_int(item.findtext("comments"))
            or _parse_int(torznab_attrs.get("comments")),
            pub_date=item.findtext("pubDate"),
            size=_parse_int(item.findtext("size"))
            or _parse_int(torznab_attrs.get("size")),
            link=item.findtext("link"),
            categories=categories,
            tags=tags,
            files=files,
            poster=torznab_attrs.get("poster"),
            group=torznab_attrs.get("group"),
            team=torznab_attrs.get("team"),
            seeders=_parse_int(torznab_attrs.get("seeders")),
            leechers=_parse_int(torznab_attrs.get("leechers")),
            peers=_parse_int(torznab_attrs.get("peers")),
            grabs=_parse_int(torznab_attrs.get("grabs")),
            infohash=torznab_attrs.get("infohash"),
            magnet_url=torznab_attrs.get("magneturl"),
            seed_type=torznab_attrs.get("seedtype"),
            dl_volume_factor=_parse_float(
                torznab_attrs.get("downloadvolumefactor"), default=1.0
            ),
            ul_volume_factor=_parse_float(
                torznab_attrs.get("uploadvolumefactor"), default=1.0
            ),
            min_ratio=_parse_float(torznab_attrs.get("minimumratio")),
            min_seed_time=_parse_float(torznab_attrs.get("minimumseedtime")),
            password=_parse_int(torznab_attrs.get("password")),
            nfo=_parse_int(torznab_attrs.get("nfo")),
            info=torznab_attrs.get("info"),
            year=_parse_int(torznab_attrs.get("year")),
            cover_url=torznab_attrs.get("coverurl"),
            backdrop_url=torznab_attrs.get("backdropurl"),
            media_info=_parse_media_info(torznab_attrs),
            tv_info=_parse_tv_info(torznab_attrs),
            movie_info=_parse_movie_info(torznab_attrs),
            audio_info=_parse_audio_info(torznab_attrs),
            music_info=_parse_music_info(torznab_attrs),
            book_info=_parse_book_info(torznab_attrs),
        )
        items.append(torrent)
    return items


def _parse_search_mode(elem: ET.Element | None) -> SearchMode | None:
    if elem is None:
        return None
    params = elem.get("supportedParams")
    return SearchMode(
        available=_parse_bool(elem.get("available")),
        supported_params=params.split(",") if params else [],
    )


def parse_capabilities(xml_string: str) -> Capabilities:
    root = ET.fromstring(xml_string)
    _check_for_error(root)

    server = None
    if (elem := root.find("server")) is not None:
        server = Server(
            version=elem.get("version"),
            title=elem.get("title"),
            strapline=elem.get("strapline"),
            email=elem.get("email"),
            url=elem.get("url"),
            image=elem.get("image"),
        )

    limits = None
    if (elem := root.find("limits")) is not None:
        limits = Limits(
            max=_parse_int(elem.get("max")),
            default=_parse_int(elem.get("default")),
        )

    registration = None
    if (elem := root.find("registration")) is not None:
        registration = Registration(
            available=_parse_bool(elem.get("available")),
            open=_parse_bool(elem.get("open")),
        )

    searching = None
    if (searching_elem := root.find("searching")) is not None:
        searching = Searching(
            search=_parse_search_mode(searching_elem.find("search")),
            tv_search=_parse_search_mode(searching_elem.find("tv-search")),
            movie_search=_parse_search_mode(searching_elem.find("movie-search")),
            audio_search=_parse_search_mode(searching_elem.find("audio-search")),
            book_search=_parse_search_mode(searching_elem.find("book-search")),
        )

    categories = []
    for cat in root.findall("categories/category"):
        subcats = [
            SubCategory(id=_parse_int(subcat.get("id")), name=subcat.get("name"))
            for subcat in cat.findall("subcat")
        ]
        categories.append(
            Category(
                id=_parse_int(cat.get("id")), name=cat.get("name"), subcats=subcats
            )
        )

    genres = [
        Genre(
            id=_parse_int(genre.get("id")),
            category_id=_parse_int(genre.get("categoryid")),
            name=genre.get("name"),
        )
        for genre in root.findall("genres/genre")
    ]

    tags = [
        Tag(name=tag.get("name"), description=tag.get("description"))
        for tag in root.findall("tags/tag")
    ]

    return Capabilities(
        server=server,
        limits=limits,
        registration=registration,
        searching=searching,
        categories=categories,
        genres=genres,
        tags=tags,
    )
