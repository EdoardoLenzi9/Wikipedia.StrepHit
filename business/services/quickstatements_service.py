import os, datetime, re, json, time, sys
from domain.models.quick_statement import QuickStatement, Qualifier, Source, Command
from domain.mapping import LinkMapping
import domain.mapping as mapping
import business.services.url_service as url_svc
import business.queries.sitelink_queries as query

def update_references (input_file, output_file, error_file):
    if not exists(input_file) :
        raise Exception("file: {0} not found".format(input_file))

    with open(input_file) as file:
        rows = file.readlines() 
        index = 0
        total = len(rows)
        for row in rows:
            index += 1
            progress(index, total)
            try:  
                sitelink = get_link(row)
                if sitelink != None :
                    reference = generate_db_reference(sitelink)
                    log(output_file, "{0}\t{1}".format(row, reference))
                else :
                    log(error_file, "No sitelink at line \t {0}".format(row))

            except :
                print('An error occurs reading {0} file, at line: \n {1} \n'.format(input_file, row))  
        mapping.export_mappings()

def get_link (row): #TODO now get first link, improve version for multiple links (if possible?) 
    content = [x.strip() for x in row.strip().split('\t')]
    index = 2
    while (index < len(content) -1):
        index += 1
        key = content[index]
        index += 1
        value = content[index]
        
        if(key == "S854"): # "Reference URL"
            return value.replace('"', '')
    return None

def is_unknown_source(domain, sitelink):
    if mapping.UNKNOWN_SOURCE_MAPPING.get(domain) != None : 
        for unknown_source in mapping.UNKNOWN_SOURCE_MAPPING[domain]:
            if unknown_source in sitelink: 
                return True
    return False 

def generate_db_reference(sitelink):
    domain = url_svc.get_domain(sitelink)
    if(is_unknown_source(domain, sitelink)) :
        return ""
    try: 
        for link_mapping in mapping.SOURCE_MAPPING[domain] :
            if url_svc.validate_url_template(sitelink, link_mapping.url_pattern) : #todo case like more than one $1
                url_pattern = link_mapping.url_pattern.split("$1")
                content = sitelink.replace(url_pattern[0], "").replace(url_pattern[1], "")
                return "S248\t{0}\t{1}\t{2}\tS813\t{3}".format(link_mapping.db_id, link_mapping.db_property, content, get_iso_time())
        raise Exception("mapping not found ")
    except : 
        return new_mapping(domain, sitelink)

def new_mapping(domain, sitelink): #mappo solo quello che me lo valida
    db_id = None
    db_property = None
    url_pattern = None
    try:
        result = query.get_item(domain) #TODO da ottimizzare per la categoria

        if len(result) != 0 :

            for row in result :
                db_id = get_identifier(row.subjects.value, "Q")
                if hasattr(row, 'wikidataProperty') and hasattr(row, 'formatterUrlLabel'):
                    db_property = get_identifier(row.wikidataProperty.value, "P").replace("P", "S") 
                    url_pattern = row.formatterUrlLabel.value
                    if url_svc.validate_url_template(sitelink, url_pattern) : #todo case like more than $1
                        pattern = url_pattern.split("$1")
                        content = sitelink.replace(pattern[0], "").replace(pattern[1], "")
                        mapping.add_source(domain, LinkMapping(db_id, db_property, url_pattern))
                        return "S248\t{0}\t{1}\t{2}\tS813\t{3}".format(db_id, db_property, content, get_iso_time())
        raise Exception("db domain not found in wikidata")
    except : 
        regex = re.compile("{0}/[^/]+".format(domain))
        uri = regex.search(sitelink).group(0)  
        while uri != "" :
            result = query.get_item(uri)
            if len(result) == 0 :
                mapping.add_unknown_source(domain, uri)
                break
            regex = re.compile("{0}/[^/]+".format(uri))
            uri = regex.search(sitelink).group(0)  
        if(db_id != None):
            return "S248\t{0}\tS813\t{1}".format(db_id, get_iso_time())
        return ""

def get_identifier(url, first_letter) :
    regex = re.compile(first_letter + ".*")
    return regex.search(url).group(0)  

def log(file, text):
    with open(file, 'ab+') as f:
            f.write("{0}\n".format(text))

def exists(file):
    return os.path.isfile(file)

def get_iso_time(time = datetime.datetime.now()):
    return "{0}Z/14".format(time.replace(microsecond=0).isoformat())

def progress(count, total, suffix=''):
	bar_len = 60
	filled_len = int(round(bar_len * count / float(total)))

	percents = round(100.0 * count / float(total), 1)
	bar = '=' * filled_len + '-' * (bar_len - filled_len)

	sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
	sys.stdout.flush()  

