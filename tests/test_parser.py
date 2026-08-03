import pytest

from torznab.parser import parse_torznab


@pytest.fixture
def make_xml():
    """Helper fixture to wrap item XML snippets into a standard Torznab RSS envelope."""

    def _make(items_body: str) -> str:
        return f"""
        <rss xmlns:torznab="http://torznab.com/schemas/2015/feed">
          <channel>
            {items_body}
          </channel>
        </rss>
        """

    return _make


@pytest.fixture
def tv_sample_xml(make_xml):
    """Fixture providing a sample TV show Torznab item XML."""
    items = """
    <item>
      <title>Breaking Bad S05E14 1080p HDTV</title>
      <guid>tv-item-123</guid>
      <torznab:attr name="season" value="5" />
      <torznab:attr name="episode" value="14" />
      <torznab:attr name="rageid" value="18164" />
      <torznab:attr name="tvtitle" value="Breaking Bad" />
      <torznab:attr name="tvairdate" value="Sun, 15 Sep 2013 00:00:00 +0000" />
      <torznab:attr name="tvdbid" value="81189" />
      <torznab:attr name="tvmazeid" value="169" />
      <torznab:attr name="resolution" value="1080p" />
      <torznab:attr name="video" value="x264" />
    </item>
    """
    return make_xml(items)


@pytest.fixture
def movie_sample_xml(make_xml):
    """Fixture providing a sample Movie Torznab item XML."""
    items = """
    <item>
      <title>Inception 2010 1080p Bluray</title>
      <guid>movie-item-456</guid>
      <torznab:attr name="imdb" value="1375666" />
      <torznab:attr name="imdbscore" value="8.8" />
      <torznab:attr name="imdbtitle" value="Inception" />
      <torznab:attr name="imdbtagline" value="Your mind is the scene of the crime." />
      <torznab:attr name="imdbplot" value="A thief who steals corporate secrets." />
      <torznab:attr name="imdbyear" value="2010" />
      <torznab:attr name="imdbdirector" value="Christopher Nolan" />
      <torznab:attr name="imdbactors" value="Leonardo DiCaprio, Joseph Gordon-Levitt" />
      <torznab:attr name="genre" value="Action, Sci-Fi" />
      <torznab:attr name="resolution" value="1080p" />
      <torznab:attr name="video" value="x264" />
      <torznab:attr name="audio" value="DTS" />
      <torznab:attr name="language" value="English" />
    </item>
    """
    return make_xml(items)


@pytest.fixture
def music_sample_xml(make_xml):
    """Fixture providing a sample Music Torznab item XML."""
    items = """
    <item>
      <title>Daft Punk - Random Access Memories (2013) FLAC</title>
      <guid>music-item-789</guid>
      <torznab:attr name="artist" value="Daft Punk" />
      <torznab:attr name="album" value="Random Access Memories" />
      <torznab:attr name="publisher" value="Columbia" />
      <torznab:attr name="tracks" value="Give Life Back to Music|Get Lucky" />
      <torznab:attr name="audio" value="FLAC" />
      <torznab:attr name="language" value="English" />
    </item>
    """
    return make_xml(items)


@pytest.fixture
def book_sample_xml(make_xml):
    """Fixture providing a sample Book Torznab item XML."""
    items = """
    <item>
      <title>The Hobbit by J.R.R. Tolkien EPUB</title>
      <guid>book-item-101</guid>
      <torznab:attr name="booktitle" value="The Hobbit" />
      <torznab:attr name="publishdate" value="1937-09-21" />
      <torznab:attr name="author" value="J.R.R. Tolkien" />
      <torznab:attr name="pages" value="310" />
    </item>
    """
    return make_xml(items)


@pytest.fixture
def general_torrent_sample_xml(make_xml):
    """Fixture providing a sample Torznab item with general attributes."""
    items = """
    <item>
      <title>Ubuntu 24.04 LTS Desktop ISO</title>
      <guid>ubuntu-2404</guid>
      <link>http://example.com/ubuntu.torrent</link>
      <size>4000000000</size>
      <comments>15</comments>
      <pubDate>Mon, 22 Apr 2024 10:00:00 +0000</pubDate>
      <category>5000</category>
      <category>5070</category>
      <torznab:attr name="seeders" value="120" />
      <torznab:attr name="leechers" value="10" />
      <torznab:attr name="peers" value="130" />
      <torznab:attr name="grabs" value="450" />
      <torznab:attr name="infohash" value="a1b2c3d4e5f678901234567890abcdef12345678" />
      <torznab:attr name="magneturl" value="magnet:?xt=urn:btih:a1b2c3d4e5" />
      <torznab:attr name="seedtype" value="ratio" />
      <torznab:attr name="downloadvolumefactor" value="0.0" />
      <torznab:attr name="uploadvolumefactor" value="1.0" />
      <torznab:attr name="minimumratio" value="1.5" />
      <torznab:attr name="minimumseedtime" value="86400" />
      <torznab:attr name="poster" value="http://example.com/poster.jpg" />
      <torznab:attr name="group" value="LinuxReleases" />
      <torznab:attr name="team" value="Canonical" />
      <torznab:attr name="tag" value="freeleech" />
      <torznab:attr name="tag" value="iso" />
      <torznab:attr name="files" value="1" />
      <torznab:attr name="password" value="0" />
      <torznab:attr name="nfo" value="1" />
      <torznab:attr name="info" value="http://example.com/ubuntu.nfo" />
      <torznab:attr name="year" value="2024" />
      <torznab:attr name="coverurl" value="http://example.com/cover.jpg" />
      <torznab:attr name="backdropurl" value="http://example.com/backdrop.jpg" />
    </item>
    """
    return make_xml(items)


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
