from torznab import TorrentItem


def test_torrent_item_is_freeleech():
    free_item = TorrentItem(dl_volume_factor=0.0)
    assert free_item.is_freeleech is True

    normal_item = TorrentItem(dl_volume_factor=1.0)
    assert normal_item.is_freeleech is False
