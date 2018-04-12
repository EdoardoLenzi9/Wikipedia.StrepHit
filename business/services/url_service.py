import urllib, urllib2, json, re
from collections import namedtuple
import domain.localizations as loc

def sparql_get(query):
    parameters = [('query', query)]
    headers = [Header('Accept', 'application/sparql-results+json')]
    response = http_call(loc.sparql_url, parameters, headers=headers)
    contents = response.replace("-", "_").replace('\n',' ').replace("xml:lang","xml_lang")
    content = json_deserialize(contents)
    return content.results.bindings

def json_deserialize(serialized_json):
    return json.loads(serialized_json, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

def http_call(base_url, parameters, method = "GET", headers = []):
    #opener = urllib2.build_opener(urllib2.HTTPHandler)
    params = urllib.urlencode(parameters, doseq=True)
    request = urllib2.Request("{0}?{1}".format(base_url, params))
    request.get_method = lambda: method
    for header in headers :
        request.add_header(header.key, header.value)
    return urllib2.urlopen(request).read()


def get_domain (url):
    return url.split("//")[-1].split("/")[0].split('?')[0]

def validate_url_template(sitelink, link_mapping):
    pattern = re.compile(link_mapping.url_pattern.replace("$1", ".*"))
    if(pattern.match(sitelink)):
    	return True 
    else :
	    return False

class Header(object):
    key = ""
    value = ""

    def __init__(self, key, value):
        self.key = key
        self.value = value