import json
import business.services.file_service as file_svc

def add_source(domain, source):
    if SOURCE_MAPPING.get(domain) == None : 
        SOURCE_MAPPING[domain] = [source]   
    else :                         
        SOURCE_MAPPING[domain].append(source)

def add_unknown_source(domain, unknown_source):
    if UNKNOWN_SOURCE_MAPPING.get(domain) == None : 
        UNKNOWN_SOURCE_MAPPING[domain] = [unknown_source]   
    else :                         
        UNKNOWN_SOURCE_MAPPING[domain].append(unknown_source)

def export_mappings(output_file="mappings.json"):
    source_mapping = json.dumps(SOURCE_MAPPING, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    unknown_source_mapping = json.dumps(UNKNOWN_SOURCE_MAPPING, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    file_svc.log(output_file, source_mapping)
    file_svc.log(output_file, unknown_source_mapping)

# source domain : [source QID, PID of source ID]

SOURCE_MAPPING = {
    "adb.anu.edu.au": [ LinkMapping("Q672680", "S1907", "http://adb.anu.edu.au/biography/$1") ],
    "archive.org": [ LinkMapping("Q461", "S724", "https://archive.org/details/$1") ],
    "collection.britishmuseum.org": [ LinkMapping("Q34753751", None, None) ],
    "collection.cooperhewitt.org": [ LinkMapping("Q1129820", "S2011", "https://collection.cooperhewitt.org/people/$1/") ],
    "dictionaryofarthistorians.org": [ LinkMapping("Q17166797", "S2332", "https://dictionaryofarthistorians.org/$1.html") ],
    "en.wikisource.org": [ LinkMapping("Q15156406", None, None) ],
    "gameo.org": [ LinkMapping("Q1531559", "S1842", "http://gameo.org/index.php?title=$1") ],
    "munksroll.rcplondon.ac.uk": [ LinkMapping("Q6936720", "S2941", "http://munksroll.rcplondon.ac.uk/Biography/Details/$1") ],
    "rkd.nl": [ LinkMapping("Q17299517", "S650", "https://rkd.nl/en/explore/artists/$1") ],
    "structurae.net": [ LinkMapping("Q1061861", "S2418", "https://structurae.de/personen/$1") ],
    "vocab.getty.edu": [ LinkMapping("Q2494649", "S245", "http://vocab.getty.edu/page/ulan/$1") ],
    "www.bbc.co.uk": [ LinkMapping("Q7257339", "S1367", "https://artuk.org/discover/artworks/search/actor:$1") ],
    "www.genealogics.org": [ LinkMapping("Q19847326", "S1819", "http://www.genealogics.org/getperson.php?personID=$1&tree=LEO") ],
    "www.museothyssen.org": [ LinkMapping("Q176251", "S2431", "http://www.museothyssen.org/en/thyssen/ficha_artista/$1") ],
    "www.newulsterbiography.co.uk": [ LinkMapping("Q21814517", "S2029", "http://www.newulsterbiography.co.uk/index.php/home/viewPerson/$1") ],
    "www.nndb.com": [ LinkMapping("Q1373513", "S1263", "http://www.nndb.com/people/$1/") ],
    "www.uni-stuttgart.de": [ LinkMapping("Q21417186", "S2349", "http://www.uni-stuttgart.de/hi/gnt/dsi2/index.php?table_name=dsi&function=details&where_field=id&where_value=$1") ],
    "www.wga.hu": [ LinkMapping("Q1464063", "S1882", "https://tools.wmflabs.org/mix-n-match/api.php?query=redirect&catalog=11&ext_id=$1") ],
    "yba.llgc.org.uk": [ LinkMapping("Q5273977", "S1648", "http://yba.llgc.org.uk/en/$1") ]
} 

# source domain : [unknown_uri]

UNKNOWN_SOURCE_MAPPING = {
    #"archive.org": [ "https://archive.org/download" ],
} 

class LinkMapping(object):
    db_id = ""
    db_property = ""
    url_pattern = ""

    def __init__(self, db_id, db_property, url_pattern):
        self.db_id = db_id
        self.db_property = db_property
        self.url_pattern = url_pattern