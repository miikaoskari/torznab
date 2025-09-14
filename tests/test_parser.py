from torznab.parser import parse_torznab

def test_parse_torznab_single_item_with_attrs():
    xml = """
    <rss xmlns:torznab="http://torznab.com/schemas/2015/feed">
      <channel>
        <item>
          <title>Test Title</title>
          <guid>12345</guid>
          <link>http://example.com/item/12345</link>
          <size>987654</size>
          <category>5070</category>
          <category>131088</category>
          <category>2020</category>
          <torznab:attr name="seeders" value="10"/>
          <torznab:attr name="peers" value="20"/>
          <torznab:attr name="tag" value="freeleech" />
          <torznab:attr name="seeders" value="4" />
          <torznab:attr name="grabs" value="32" />
          <torznab:attr name="peers" value="4" />
          <torznab:attr name="infohash" value="1234567890" />
          <torznab:attr name="downloadvolumefactor" value="0" />
          <torznab:attr name="uploadvolumefactor" value="1" />
        </item>
      </channel>
    </rss>
    """
    result = parse_torznab(xml)
    assert len(result) == 1
    item = result[0]
    assert item.title == "Test Title"
    assert item.guid == "12345"
    assert item.link == "http://example.com/item/12345"
    assert item.size == 987654
    assert item.categories
    assert len(item.categories) == 3
    assert item.categories[0] == 5070
    assert item.categories[1] == 131088
    assert item.categories[2] == 2020
    assert item.seeders == 4
    assert item.peers == 4
    assert item.grabs == 32
    assert item.tags
    assert item.tags[0] == "freeleech"
    assert item.infohash == "1234567890"
    assert item.dl_volume_factor == 0
    assert item.ul_volume_factor == 1

def test_parse_torznab_empty_xml():
    xml = "<rss></rss>"
    result = parse_torznab(xml)
    assert result == []
