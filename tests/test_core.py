from unittest.mock import MagicMock, patch

import pytest
import requests

from torznab import Capabilities, TorrentItem, Torznab, TorznabException


def test_api_key_is_set():
    client = Torznab(api_key="test-key")

    assert client.api_key == "test-key"


def test_api_key_gets_overridden():
    client = Torznab(api_key="default-key")

    mock_response = MagicMock()
    mock_response.text = "<rss><channel></channel></rss>"
    mock_response.raise_for_status.return_value = None

    with patch.object(client.session, "get", return_value=mock_response) as mock_get:
        client.search_torrent(
            query="ubuntu",
            url="https://indexer.example.com/api",
            api_key="custom-key",
        )

        mock_get.assert_called_once_with(
            "https://indexer.example.com/api",
            params={"t": "search", "q": "ubuntu", "apikey": "custom-key"},
        )


def test_search_torrent_success():
    xml_response = """
    <rss xmlns:torznab="http://torznab.com/schemas/2015/feed">
      <channel>
        <item>
          <title>Ubuntu 24.04 ISO</title>
          <guid>ubuntu-24.04</guid>
          <link>https://example.com/download/ubuntu.torrent</link>
          <size>4000000000</size>
        </item>
      </channel>
    </rss>
    """
    client = Torznab(api_key="default-key")

    mock_response = MagicMock()
    mock_response.text = xml_response
    mock_response.raise_for_status.return_value = None

    with patch.object(client.session, "get", return_value=mock_response) as mock_get:
        results = client.search_torrent(
            query="ubuntu",
            url="https://indexer.example.com/api",
            api_key=None,
        )

        mock_get.assert_called_once_with(
            "https://indexer.example.com/api",
            params={"t": "search", "q": "ubuntu", "apikey": "default-key"},
        )
        assert len(results) == 1
        assert isinstance(results[0], TorrentItem)
        assert results[0].title == "Ubuntu 24.04 ISO"
        assert results[0].size == 4000000000


def test_search_torrent_override_api_key():
    client = Torznab(api_key="default-key")

    mock_response = MagicMock()
    mock_response.text = "<rss><channel></channel></rss>"
    mock_response.raise_for_status.return_value = None

    with patch.object(client.session, "get", return_value=mock_response) as mock_get:
        client.search_torrent(
            query="linux",
            url="https://indexer.example.com/api",
            api_key="custom-key",
        )

        mock_get.assert_called_once_with(
            "https://indexer.example.com/api",
            params={"t": "search", "q": "linux", "apikey": "custom-key"},
        )


def test_search_torrent_invalid_url():
    client = Torznab(api_key="test-key")

    with pytest.raises(TorznabException):
        client.search_torrent(query="ubuntu", url="invalid-url", api_key=None)


def test_search_torrent_http_error():
    client = Torznab(api_key="test-key")

    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")

    with patch.object(client.session, "get", return_value=mock_response):
        with pytest.raises(TorznabException):
            client.search_torrent(
                query="ubuntu",
                url="https://indexer.example.com/api",
                api_key=None,
            )


def test_search_torrent_without_api_key():
    client = Torznab()

    mock_response = MagicMock()
    mock_response.text = "<rss><channel></channel></rss>"
    mock_response.raise_for_status.return_value = None

    with patch.object(client.session, "get", return_value=mock_response) as mock_get:
        client.search_torrent("ubuntu", "https://indexer.example.com/api")

        mock_get.assert_called_once_with(
            "https://indexer.example.com/api",
            params={"t": "search", "q": "ubuntu"},
        )


def test_get_capabilities(full_caps_xml):
    client = Torznab(api_key="test-key")

    mock_response = MagicMock()
    mock_response.text = full_caps_xml
    mock_response.raise_for_status.return_value = None

    with patch.object(client.session, "get", return_value=mock_response) as mock_get:
        caps = client.get_capabilities(url="https://indexer.example.com/api")

        mock_get.assert_called_once_with(
            "https://indexer.example.com/api",
            params={"t": "caps", "apikey": "test-key"},
        )
        assert isinstance(caps, Capabilities)
        assert caps.server is not None
        assert caps.server.title == "Example Indexer"
        assert caps.limits is not None
        assert caps.limits.max == 100
        assert len(caps.categories) == 2
        assert len(caps.tags) == 3


def test_get_capabilities_http_error():
    client = Torznab(api_key="test-key")

    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")

    with patch.object(client.session, "get", return_value=mock_response):
        with pytest.raises(TorznabException):
            client.get_capabilities(
                url="https://indexer.example.com/api",
                api_key=None,
            )
