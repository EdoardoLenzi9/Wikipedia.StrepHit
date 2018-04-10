import urllib, urllib2, json
from collections import namedtuple
import domain.localizations as loc

def get (url):
    contents = urllib2.urlopen(encode_url(url)).read()
    contents = contents.replace("-", "_")
    content = json.loads(contents, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    return content

def get_domain (url):
    return url.split("//")[-1].split("/")[0].split('?')[0]

def encode_url (url):
    return urllib.quote(url)

# Header Accept: application/sparql-results+json are provided.