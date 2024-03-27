# Contains functions/classes for making requests to Torznab servers, handling responses, and parsing XML/JSON data.
import requests
from lxml import objectify

def caps(url, api_key=None):
    # Get capabilities
    payload = {}
    headers = {}
    response = None

    if api_key is not None:
        # Request with apikey
        caps = f"?t=caps&apikey={api_key}"
        response = requests.request("GET", url + caps, headers=headers, data=payload)
    else:
        # Request without apikey
        caps = f"?t=caps"
        response = requests.request("GET", url + caps, headers=headers, data=payload)
    
    xml_content = response.content
    tree = objectify.fromstring(xml_content)

    return tree

def search():

    pass

def tv_search():
    pass

def movie():
    pass

def music():
    pass

def book():
    pass

