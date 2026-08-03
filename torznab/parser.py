import xml.etree.ElementTree as ET

from .types import (
    AudioInfo,
    BookInfo,
    MediaInfo,
    MovieInfo,
    MusicInfo,
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
