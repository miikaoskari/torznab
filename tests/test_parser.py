import pytest

from torznab.exceptions import TorznabAPIError
from torznab.parser import parse_capabilities, parse_torznab


def test_parse_tv_sample(tv_sample_xml):
    results = parse_torznab(tv_sample_xml)
    assert len(results) == 1
    item = results[0]

    assert item.title == "Breaking Bad S05E14 1080p HDTV"
    assert item.guid == "tv-item-123"

    assert item.tv_info is not None
    assert item.tv_info.season == 5
    assert item.tv_info.episode == 14
    assert item.tv_info.rage_id == 18164
    assert item.tv_info.tv_title == "Breaking Bad"
    assert item.tv_info.airdate == "Sun, 15 Sep 2013 00:00:00 +0000"
    assert item.tv_info.tvdb_id == 81189
    assert item.tv_info.tvmaze_id == 169

    assert item.media_info is not None
    assert item.media_info.resolution == "1080p"
    assert item.media_info.video == "x264"

    # Other category sub-models should be None
    assert item.movie_info is None
    assert item.music_info is None
    assert item.book_info is None


def test_parse_movie_sample(movie_sample_xml):
    results = parse_torznab(movie_sample_xml)
    assert len(results) == 1
    item = results[0]

    assert item.title == "Inception 2010 1080p Bluray"
    assert item.guid == "movie-item-456"

    assert item.movie_info is not None
    assert item.movie_info.imdb_id == "1375666"
    assert item.movie_info.imdb_score == "8.8"
    assert item.movie_info.imdb_title == "Inception"
    assert item.movie_info.imdb_tagline == "Your mind is the scene of the crime."
    assert item.movie_info.imdb_plot == "A thief who steals corporate secrets."
    assert item.movie_info.imdb_year == 2010
    assert item.movie_info.imdb_director == "Christopher Nolan"
    assert item.movie_info.imdb_actors == "Leonardo DiCaprio, Joseph Gordon-Levitt"

    assert item.media_info is not None
    assert item.media_info.genre == "Action, Sci-Fi"
    assert item.media_info.resolution == "1080p"
    assert item.media_info.video == "x264"

    assert item.audio_info is not None
    assert item.audio_info.audio == "DTS"
    assert item.audio_info.language == "English"

    # Other category sub-models should be None
    assert item.tv_info is None
    assert item.music_info is None
    assert item.book_info is None


def test_parse_music_sample(music_sample_xml):
    results = parse_torznab(music_sample_xml)
    assert len(results) == 1
    item = results[0]

    assert item.title == "Daft Punk - Random Access Memories (2013) FLAC"
    assert item.guid == "music-item-789"

    assert item.music_info is not None
    assert item.music_info.artist == "Daft Punk"
    assert item.music_info.album == "Random Access Memories"
    assert item.music_info.publisher == "Columbia"
    assert item.music_info.tracks == "Give Life Back to Music|Get Lucky"

    assert item.audio_info is not None
    assert item.audio_info.audio == "FLAC"
    assert item.audio_info.language == "English"

    # Other category sub-models should be None
    assert item.tv_info is None
    assert item.movie_info is None
    assert item.book_info is None


def test_parse_book_sample(book_sample_xml):
    results = parse_torznab(book_sample_xml)
    assert len(results) == 1
    item = results[0]

    assert item.title == "The Hobbit by J.R.R. Tolkien EPUB"
    assert item.guid == "book-item-101"

    assert item.book_info is not None
    assert item.book_info.book_title == "The Hobbit"
    assert item.book_info.publish_date == "1937-09-21"
    assert item.book_info.author == "J.R.R. Tolkien"
    assert item.book_info.pages == 310

    # Other category sub-models should be None
    assert item.tv_info is None
    assert item.movie_info is None
    assert item.music_info is None


def test_parse_general_torrent_sample(general_torrent_sample_xml):
    results = parse_torznab(general_torrent_sample_xml)
    assert len(results) == 1
    item = results[0]

    assert item.title == "Ubuntu 24.04 LTS Desktop ISO"
    assert item.guid == "ubuntu-2404"
    assert item.link == "http://example.com/ubuntu.torrent"
    assert item.size == 4000000000
    assert item.comments == 15
    assert item.categories == [5000, 5070]
    assert item.seeders == 120
    assert item.leechers == 10
    assert item.peers == 130
    assert item.grabs == 450
    assert item.infohash == "a1b2c3d4e5f678901234567890abcdef12345678"
    assert item.magnet_url == "magnet:?xt=urn:btih:a1b2c3d4e5"
    assert item.seed_type == "ratio"
    assert item.dl_volume_factor == 0.0
    assert item.ul_volume_factor == 1.0
    assert item.min_ratio == 1.5
    assert item.min_seed_time == 86400.0
    assert item.poster == "http://example.com/poster.jpg"
    assert item.group == "LinuxReleases"
    assert item.team == "Canonical"
    assert item.tags == ["freeleech", "iso"]
    assert item.files == [1]
    assert item.password == 0
    assert item.nfo == 1
    assert item.info == "http://example.com/ubuntu.nfo"
    assert item.year == 2024
    assert item.cover_url == "http://example.com/cover.jpg"
    assert item.backdrop_url == "http://example.com/backdrop.jpg"
    assert item.is_freeleech is True


def test_parse_torznab_empty_xml():
    xml = "<rss></rss>"
    result = parse_torznab(xml)
    assert result == []


def test_parse_torznab_invalid_numeric_values(make_xml):
    xml = make_xml("""
    <item>
      <title>Test Title</title>
      <comments>invalid_int</comments>
      <torznab:attr name="downloadvolumefactor" value="invalid_float" />
    </item>
    """)
    result = parse_torznab(xml)
    assert len(result) == 1
    assert result[0].comments is None
    assert result[0].dl_volume_factor == 1.0


def test_parse_capabilities_server(full_caps_xml):
    caps = parse_capabilities(full_caps_xml)

    assert caps.server is not None
    assert caps.server.version == "1.1"
    assert caps.server.title == "Example Indexer"
    assert caps.server.strapline == "A fine indexer"
    assert caps.server.email == "admin@indexer.local"
    assert caps.server.url == "http://indexer.local/"
    assert caps.server.image == "http://indexer.local/content/banner.jpg"


def test_parse_capabilities_limits(full_caps_xml):
    caps = parse_capabilities(full_caps_xml)

    assert caps.limits is not None
    assert caps.limits.max == 100
    assert caps.limits.default == 50


def test_parse_capabilities_registration(full_caps_xml):
    caps = parse_capabilities(full_caps_xml)

    assert caps.registration is not None
    assert caps.registration.available is True
    assert caps.registration.open is False


def test_parse_capabilities_searching(full_caps_xml):
    caps = parse_capabilities(full_caps_xml)

    assert caps.searching is not None

    assert caps.searching.search is not None
    assert caps.searching.search.available is True
    assert caps.searching.search.supported_params == ["q"]

    assert caps.searching.tv_search is not None
    assert caps.searching.tv_search.available is True
    assert caps.searching.tv_search.supported_params == [
        "q",
        "rid",
        "tvdbid",
        "season",
        "ep",
    ]

    assert caps.searching.movie_search is not None
    assert caps.searching.movie_search.available is False
    assert caps.searching.movie_search.supported_params == ["q", "imdbid", "genre"]

    assert caps.searching.audio_search is not None
    assert caps.searching.audio_search.available is False
    assert caps.searching.audio_search.supported_params == ["q"]

    assert caps.searching.book_search is not None
    assert caps.searching.book_search.available is False
    assert caps.searching.book_search.supported_params == ["q"]


def test_parse_capabilities_categories(full_caps_xml):
    caps = parse_capabilities(full_caps_xml)

    assert len(caps.categories) == 2

    movies = caps.categories[0]
    assert movies.id == 2000
    assert movies.name == "Movies"
    assert len(movies.subcats) == 1
    assert movies.subcats[0].id == 2010
    assert movies.subcats[0].name == "Foreign"

    tv = caps.categories[1]
    assert tv.id == 5000
    assert tv.name == "TV"
    assert len(tv.subcats) == 2
    assert tv.subcats[0].id == 5040
    assert tv.subcats[0].name == "HD"
    assert tv.subcats[1].id == 5070
    assert tv.subcats[1].name == "Anime"


def test_parse_capabilities_genres(full_caps_xml):
    caps = parse_capabilities(full_caps_xml)

    assert len(caps.genres) == 1
    assert caps.genres[0].id == 1
    assert caps.genres[0].category_id == 5000
    assert caps.genres[0].name == "Kids"


def test_parse_capabilities_tags(full_caps_xml):
    caps = parse_capabilities(full_caps_xml)

    assert len(caps.tags) == 3
    assert caps.tags[0].name == "anonymous"
    assert caps.tags[0].description == "Uploader is anonymous"
    assert caps.tags[1].name == "trusted"
    assert caps.tags[1].description == "Uploader has high reputation"
    assert caps.tags[2].name == "internal"
    assert caps.tags[2].description == "Uploader is an internal release group"


def test_parse_capabilities_minimal(minimal_caps_xml):
    caps = parse_capabilities(minimal_caps_xml)

    assert caps.server is None
    assert caps.limits is None
    assert caps.registration is None
    assert caps.searching is None
    assert caps.categories == []
    assert caps.genres == []
    assert caps.tags == []


def test_parse_capabilities_registration_missing_attrs():
    xml = """
    <caps>
       <registration />
    </caps>
    """
    caps = parse_capabilities(xml)

    assert caps.registration is not None
    assert caps.registration.available is None
    assert caps.registration.open is None


def test_parse_torznab_api_error():
    xml = '<error code="100" description="Incorrect user credentials" />'

    with pytest.raises(TorznabAPIError) as exc_info:
        parse_torznab(xml)

    assert exc_info.value.code == 100
    assert exc_info.value.description == "Incorrect user credentials"


def test_parse_capabilities_api_error():
    xml = '<error code="901" description="API Request Limit Reached" />'

    with pytest.raises(TorznabAPIError) as exc_info:
        parse_capabilities(xml)

    assert exc_info.value.code == 901
    assert exc_info.value.description == "API Request Limit Reached"


def test_parse_capabilities_search_mode_missing_supported_params():
    xml = """
    <caps>
       <searching>
          <search available="yes" />
       </searching>
    </caps>
    """
    caps = parse_capabilities(xml)

    assert caps.searching is not None
    assert caps.searching.search is not None
    assert caps.searching.search.available is True
    assert caps.searching.search.supported_params == []
    assert caps.searching.tv_search is None
    assert caps.searching.movie_search is None
    assert caps.searching.audio_search is None
    assert caps.searching.book_search is None
