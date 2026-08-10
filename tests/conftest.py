import pytest


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


@pytest.fixture
def full_caps_xml():
    """Fixture providing a complete torznab caps XML document."""
    return """
    <caps>
       <server version="1.1" title="Example Indexer" strapline="A fine indexer"
             email="admin@indexer.local" url="http://indexer.local/"
             image="http://indexer.local/content/banner.jpg" />
       <limits max="100" default="50" />
       <registration available="yes" open="no" />

       <searching>
          <search available="yes" supportedParams="q" />
          <tv-search available="yes" supportedParams="q,rid,tvdbid,season,ep" />
          <movie-search available="no" supportedParams="q,imdbid,genre" />
          <audio-search available="no" supportedParams="q" />
          <book-search available="no" supportedParams="q" />
       </searching>

       <categories>
          <category id="2000" name="Movies">
             <subcat id="2010" name="Foreign" />
          </category>
          <category id="5000" name="TV">
             <subcat id="5040" name="HD" />
             <subcat id="5070" name="Anime" />
          </category>
       </categories>

       <genres>
          <genre id="1" categoryid="5000" name="Kids" />
       </genres>

       <tags>
          <tag name="anonymous" description="Uploader is anonymous" />
          <tag name="trusted" description="Uploader has high reputation" />
          <tag name="internal" description="Uploader is an internal release group" />
       </tags>
    </caps>
    """


@pytest.fixture
def minimal_caps_xml():
    """Fixture providing a caps XML document with only the root element."""
    return "<caps></caps>"
