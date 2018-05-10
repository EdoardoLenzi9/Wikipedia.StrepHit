import os, datetime, re, time, sys, threading
import domain.mapping as mapping
import domain.localizations as loc
import business.services.url_service as url_svc
import business.queries.sitelink_queries as query
import business.services.file_service as file_svc
from domain.mapping import LinkMapping

# constants
input_file = loc.input_file 
output_file = loc.output_file
error_file = loc.error_file
log_file = loc.log_file
total = 0
index = 0

# list of unmapped url
def export_unmapped_url_list ():
    if not file_svc.exists(input_file) :
        raise Exception("file: {0} not found".format(input_file))

    mapping.import_mappings()

    with open(input_file) as file:
        rows = file.readlines() 
        total = len(rows)
        index = 0
        for row in rows:
            index += 1
            progress(index, total)
            try :
                sitelink = url_svc.get_link(row)
                if sitelink != None :
                    domain = url_svc.get_domain(sitelink)
                    is_not_mapped = True
                    for link_mapping in mapping.SOURCE_MAPPING[domain] :
                        if url_svc.validate_url_template(sitelink, link_mapping.url_pattern) :
                            is_not_mapped = False
                    if(is_not_mapped) :
                        file_svc.log(output_file, row)
            except : 
                file_svc.log(output_file, row)

# refresh remapped urls
def refresh_urls (domains = []):
    foreach_domain = len(domains) == 0 
    if not file_svc.exists(input_file) :
        raise Exception("file: {0} not found".format(input_file))

    with open(input_file) as file:
        rows = file.readlines() 
        total = len(rows)
        index = 0
        for row in rows:
            index += 1
            progress(index, total)
            try :
                sitelink = url_svc.get_link(row)
                if sitelink != None :
                    if foreach_domain or (url_svc.get_domain(sitelink) in domains):
                        current_url = url_svc.refresh_url(sitelink)
                        if current_url != None :
                            row = row.replace(sitelink, current_url)
                            file_svc.log(log_file, "mapped \t {0} \t to \t {1}".format(sitelink, current_url))
                        elif loc.DELETE_ROW :
                            row = row.replace("S854\t{0}".format(sitelink), current_url)
                            file_svc.log(log_file, "deleted row (because link isn't active): \t {0}".format(row))
                row = row.replace("\n", "")
                file_svc.log(output_file, row)
            except : 
                file_svc.log(error_file, "error at row: {0}".format(row))

def add_db_references_async (isAsyncMode = loc.IS_ASYNC_MODE):
    global total
    if not file_svc.exists(loc.input_file) :
        raise Exception("file: {0} not found".format(input_file))

    mapping.import_mappings()

    with open(input_file) as file:
        rows = file.readlines() 
        total = len(rows)
        for row in rows:
            progress(index, total)
            try:  
                sitelink = url_svc.get_link(row)
                if sitelink != None :
                    if(isAsyncMode):
                        thread = threading.Thread(target=generate_db_reference_wrapper, args=(row, sitelink))
                        thread.daemon = True
                        thread.start()                       
                    else :
                        generate_db_reference_wrapper(row, sitelink)
                else :
                    file_svc.log(error_file, "No sitelink at line \t {0}".format(row))
            except :
                file_svc.log(error_file, 'An error occurs reading {0} file, at line: \n {1} \n'.format(input_file, row))

def generate_db_reference_wrapper(row, sitelink):  
    global index           
    reference = generate_db_reference(sitelink)
    if(reference == "") :
        reference = "S813\t{0}".format(get_iso_time())
    row = row.replace("\n", "")
    file_svc.log(output_file, "{0}\t{1}".format(row, reference))
    mapping.export_mappings()
    index += 1
    progress(index, total)

def generate_db_reference(sitelink, map_all_responses = loc.MAP_ALL_RESPONSES):
    domain = url_svc.get_domain(sitelink)
    if(domain == ""):
        return ""
    if(is_unknown_source(domain, sitelink)) :
        return get_db_id(domain)
    try: 
        for link_mapping in mapping.SOURCE_MAPPING[domain] :
            if url_svc.validate_url_template(sitelink, link_mapping.url_pattern) : #todo case like more than one $1
                content = url_svc.extract_placeholder(link_mapping.url_pattern, sitelink)
                return "S248\t{0}\t{1}\t\"{2}\"\tS813\t{3}".format(link_mapping.db_id, link_mapping.db_property, content, get_iso_time())
        if(map_all_responses and is_domain_just_mapped(domain)) :
            return get_db_id(domain)
        raise Exception("mapping not found ")
    except : 
        if map_all_responses:
            return mapping_all(domain, sitelink)
        return new_mapping(domain, sitelink)

def is_domain_just_mapped(domain):
    if domain not in mapping.DOMAINS_JUST_MAPPED : 
        return True
    return False 

def is_unknown_source(domain, sitelink):
    if mapping.UNKNOWN_SOURCE_MAPPING.get(domain) != None : 
        for unknown_source in mapping.UNKNOWN_SOURCE_MAPPING[domain]:
            if unknown_source in sitelink: 
                return True
    return False 

def get_db_id(domain):
    if mapping.SOURCE_MAPPING.get(domain) != None : 
        for mapping_entry in mapping.SOURCE_MAPPING[domain] :
            if mapping_entry.db_id != None :
                return "S248\t{0}\tS813\t{1}".format(mapping_entry.db_id, get_iso_time())
    return ""

def mapping_all(domain, sitelink): 
    if domain not in mapping.DOMAINS_JUST_MAPPED :
        mapping.DOMAINS_JUST_MAPPED.append(domain)
    db_id = None
    try:
        result = query.get_item(domain) 

        for row in result :
            real_domain = url_svc.get_domain(row.sitelinkLabel.value)
            db_id = get_identifier(row.subjects.value, "Q")
            db_property =  get_identifier(row.wikidataProperty.value, "P").replace("P", "S") if hasattr(row, 'wikidataProperty') else None
            url_pattern = row.formatterUrlLabel.value if  hasattr(row, 'formatterUrlLabel') else None 
            mapping.add_source(real_domain, LinkMapping(db_id, db_property, url_pattern))

        for link_mapping in mapping.SOURCE_MAPPING[domain] :
            if url_svc.validate_url_template(sitelink, link_mapping.url_pattern) : 
                content = url_svc.extract_placeholder(link_mapping.url_pattern, sitelink)
                return "S248\t{0}\t{1}\t\"{2}\"\tS813\t{3}".format(link_mapping.db_id, link_mapping.db_property, content, get_iso_time())

        if len(result) == 0:
            mapping.add_unknown_source(domain, domain)
            return ""
        raise Exception("db domain not found in wikidata")
    except : 
        regex = re.compile("{0}/[^/]+".format(domain))
        uri = regex.search(sitelink).group(0)  
        while uri != "" :
            result = query.get_item(uri)
            if len(result) == 0 :
                mapping.add_unknown_source(domain, uri)
                mapping.add_source(domain, LinkMapping(db_id, None, None))
                break
            regex = re.compile("{0}/[^/]+".format(uri))
            uri = regex.search(sitelink).group(0)  
        return get_db_id(domain)

def new_mapping(domain, sitelink): #mappo solo quello che me lo valida
    db_id = None
    try:
        result = query.get_item(domain) #TODO da ottimizzare per la categoria

        if len(result) != 0 :
            if len(result) == 1:
                row = result[0]
                if not hasattr(row, 'formatterUrlLabel') and hasattr(row, 'sitelinkLabel'):
                    domain = url_svc.get_domain(row.sitelinkLabel.value)
                    mapping.add_unknown_source(domain, domain)
                    mapping.add_source(domain, domain)
                    return get_db_id(domain)
            for row in result :
                db_id = get_identifier(row.subjects.value, "Q")
                if hasattr(row, 'wikidataProperty') and hasattr(row, 'formatterUrlLabel') and hasattr(row, 'sitelinkLabel'):
                    real_domain = url_svc.get_domain(row.sitelinkLabel.value)
                    db_property = get_identifier(row.wikidataProperty.value, "P").replace("P", "S") 
                    url_pattern = row.formatterUrlLabel.value
                    if url_svc.validate_url_template(sitelink, url_pattern) : #todo case like more than $1
                        pattern = url_pattern.split("$1")
                        content = sitelink.replace(pattern[0], "").replace(pattern[1], "")
                        mapping.add_source(real_domain, LinkMapping(db_id, db_property, url_pattern))
                        return "S248\t{0}\t{1}\t\"{2}\"\tS813\t{3}".format(db_id, db_property, content, get_iso_time())
        if len(result) == 0:
            mapping.add_unknown_source(domain, domain)
            return ""
        raise Exception("db domain not found in wikidata")
    except : 
        regex = re.compile("{0}/[^/]+".format(domain))
        uri = regex.search(sitelink).group(0)  
        while uri != "" :
            result = query.get_item(uri)
            if len(result) == 0 :
                mapping.add_unknown_source(domain, uri)
                mapping.add_source(domain, LinkMapping(db_id, None, None))
                break
            regex = re.compile("{0}/[^/]+".format(uri))
            uri = regex.search(sitelink).group(0)  
        return get_db_id(domain)

def get_identifier(url, first_letter) :
    regex = re.compile(first_letter + ".*")
    id = regex.search(url).group(0)  
    if id == "" :
        return None
    return id

def get_iso_time(time = datetime.datetime.now()):
    return "{0}Z/14".format(time.replace(microsecond=0).isoformat())

def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    try:
        sys.stdout.write('[%s] %s%s %s Processing line: %s \r' % (bar, percents, '%', suffix, count))
        sys.stdout.flush()  
    except :
        print ("\n warning: [shuld never happen error] loader-bar error count \t {0} \t total {1} \n".format(count, total))
