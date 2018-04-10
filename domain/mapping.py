# source domain : [source QID, PID of source ID]
SOURCE_MAPPING = {
    "adb.anu.edu.au": ["Q672680", "S1907"], # http://adb.anu.edu.au/biography/$1
    "archive.org": ["Q461", "S724"], # https://archive.org/details/$1
    "collection.britishmuseum.org": ["Q34753751", None],
    "collection.cooperhewitt.org": ["Q1129820", "S2011"], # https://collection.cooperhewitt.org/people/$1/
    "dictionaryofarthistorians.org": ["Q17166797", "S2332"], # https://dictionaryofarthistorians.org/$1.html
    "en.wikisource.org": ["Q15156406", None],
    "gameo.org": ["Q1531559", "S1842"], # http://gameo.org/index.php?title=$1
    "munksroll.rcplondon.ac.uk": ["Q6936720", "S2941"], # http://munksroll.rcplondon.ac.uk/Biography/Details/$1
    "rkd.nl": ["Q17299517", "S650"], # https://rkd.nl/en/explore/artists/$1
    "structurae.net": ["Q1061861", "S2418"], # https://structurae.de/personen/$1
    "vocab.getty.edu": ["Q2494649", "S245"], # http://vocab.getty.edu/page/ulan/$1
    "www.bbc.co.uk": ["Q7257339", "S1367"], # https://artuk.org/discover/artworks/search/actor:$1
    "www.genealogics.org": ["Q19847326", "S1819"], # http://www.genealogics.org/getperson.php?personID=$1&tree=LEO
    "www.museothyssen.org": ["Q176251", "S2431"], # http://www.museothyssen.org/en/thyssen/ficha_artista/$1
    "www.newulsterbiography.co.uk": ["Q21814517", "S2029"], # http://www.newulsterbiography.co.uk/index.php/home/viewPerson/$1
    "www.nndb.com": ["Q1373513", "S1263"], # http://www.nndb.com/people/$1/
    "www.uni-stuttgart.de": ["Q21417186", "S2349"], # http://www.uni-stuttgart.de/hi/gnt/dsi2/index.php?table_name=dsi&function=details&where_field=id&where_value=$1
    "www.wga.hu": ["Q1464063", "S1882"], # https://tools.wmflabs.org/mix-n-match/api.php?query=redirect&catalog=11&ext_id=$1
    "yba.llgc.org.uk": ["Q5273977", "S1648"] # http://yba.llgc.org.uk/en/$1
} #TODO multiple entries in URI
