from urlparse import urlparse

def get_domain(url):
    parsed_uri = urlparse(url)
    return '{uri.netloc}'.format(uri=parsed_uri)    