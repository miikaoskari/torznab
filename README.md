# torznab
Python library for interacting with torznab APIs.

# usage
```python
from torznab import Torznab

tn = Torznab(api_key="secretapikey")

res = tn.search_torrent("ubuntu", "https://localhost:9876/torznab")

print(res)
``` 
