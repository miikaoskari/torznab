# torznab
python library for interacting with torznab APIs.

partial implementation of the [torznab 1.3 draft spec](https://torznab.github.io/spec-1.3-draft/torznab/Specification-v1.3.html).

# usage
```python
from torznab import Torznab

tn = Torznab(api_key="secretapikey")

# or without an API key
tn = Torznab()

res = tn.search_torrent("ubuntu", "https://localhost:9876/torznab")

print(res)
```

# todo

implement the reading of rest of the endpoints:
- caps
- tvsearch
- movie
- music
- book

in the future may implement newznab endpoints as well
