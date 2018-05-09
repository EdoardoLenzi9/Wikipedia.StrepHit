import urllib, urllib2, json, re
from collections import namedtuple
import domain.localizations as loc

def refresh_url(old_url):
    try :
        response = urllib2.urlopen(old_url)
        return response.url
    except :
        return None

def sparql_get(query):
    parameters = [('query', query)]
    headers = [Header('Accept', 'application/sparql-results+json')]
    response = http_call(loc.sparql_url, parameters, headers=headers)
    response = response.replace("-", "_").replace('\n',' ').replace("xml:lang","xml_lang")
    return json_deserialize(response).results.bindings

def json_deserialize(serialized_json):
    return json.loads(serialized_json, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

def http_call(base_url, parameters, method = "GET", headers = []):
    params = urllib.urlencode(parameters, doseq=True)
    request = urllib2.Request("{0}?{1}".format(base_url, params))
    request.get_method = lambda: method
    for header in headers :
        request.add_header(header.key, header.value)
    return urllib2.urlopen(request).read()

def get_domain (url):
    return url.split("//")[-1].split("/")[0].split('?')[0]

def validate_url_template(sitelink, url_pattern):
    if(url_pattern == None) :
        return False
    pattern = re.compile(re.escape(url_pattern.encode('ascii')).replace("\\$1", ".*"))
    if(pattern.match(sitelink)):
    	return True 
    else :
	    return False

def get_link (row): 
    regex = re.compile("S854\t[^\t]+")
    link = re.sub(r'"|(S854)|\n|\t', '', regex.search(row).group(0))
    if link == "" :
        return None
    return link

def extract_placeholder(url_pattern, url): # TODO now this works only for one placeholder ($1)
    url_pattern = url_pattern.split("$1")
    return url.replace(url_pattern[0], "").replace(url_pattern[1], "")

class Header(object):
    key = ""
    value = ""

    def __init__(self, key, value):
        self.key = key
        self.value = value