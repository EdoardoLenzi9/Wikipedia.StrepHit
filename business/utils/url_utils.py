import urllib, urllib2, json, re
from collections import namedtuple
import domain.localizations as loc
from requests.utils import quote

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
    if url is not None:
        domain = url.split("//")[-1].split("/")[0].split('?')[0]
        if domain == "" :
            return None
        else :
            return domain
    return None

def validate_url_template(sitelink, url_pattern): # TODO handle cases with more than one placeholder ($1)
    if(url_pattern is None) :
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

def extract_placeholder(link_mapping, url): # TODO now this works only for one placeholder ($1)
    url_pattern = link_mapping.url_pattern.split("$1")
    content = url.replace(url_pattern[0], "").replace(url_pattern[1], "")
    if link_mapping.to_upper_case:
        return content.upper()
    return content

def build_query_url(base_url, query_parameters):
    url = "{0}?".format(base_url)
    for key, value in query_parameters.iteritems():
        url = "{0}{1}={2}&".format(url, key, percent_encoding(value))
    return url[:-1]

def percent_encoding(query):
    return quote(query, safe='')

def to_https(http_url):
    return http_url.replace("http:", "https:")

class Header(object):
    key = ""
    value = ""

    def __init__(self, key, value):
        self.key = key
        self.value = value