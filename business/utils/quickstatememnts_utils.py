import re, datetime
from business.mapping import LinkMapping

def get_identifier(url, first_letter) :
    regex = re.compile(first_letter + ".*")
    id = regex.search(url).group(0)  
    if id == "" :
        return None
    return id

def get_iso_time(time = datetime.datetime.now()):
    return "{0}Z/14".format(time.replace(microsecond=0).isoformat())

def db_reference(link_mapping = None, content = ""):  
    if link_mapping is not None and content == "":
        if not is_none_or_empty(link_mapping.db_id):
            return "S248\t{0}\tS813\t{1}".format(link_mapping.db_id, get_iso_time())
    elif link_mapping is not None and content != "":
        if not is_none_or_empty(link_mapping):
            return "S248\t{0}\t{1}\t\"{2}\"\tS813\t{3}".format(link_mapping.db_id, link_mapping.db_property, content, get_iso_time())
    return "S813\t{0}".format(get_iso_time())

def is_none_or_empty(item):
    if isinstance(item, basestring):
        return item is None or item == ""        
    elif isinstance(item, LinkMapping):
        return is_none_or_empty(item.db_id) or is_none_or_empty(item.db_property)


    