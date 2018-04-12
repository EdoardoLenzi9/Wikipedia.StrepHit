import os, datetime, re, json, time, sys
import domain.mapping as mapping
import business.services.url_service as url_svc
import business.queries.sitelink_queries as query
import business.services.file_service as file_svc
from domain.mapping import LinkMapping

def update_references (input_file, output_file, error_file, mapping_file):
    if not file_svc.exists(input_file) :
        raise Exception("file: {0} not found".format(input_file))

    with open(input_file) as file:
        rows = file.readlines() 
        index = 0
        total = len(rows)
        for row in rows:
            index += 1
            progress(index, total)
            try:  
                sitelink = url_svc.get_link(row)
                if sitelink != None :
                    reference = generate_db_reference(sitelink)
                    file_svc.log(output_file, "{0}\t{1}".format(row, reference))
                else :
                    file_svc.log(error_file, "No sitelink at line \t {0}".format(row))
            except :
                file_svc.log(error_file, 'An error occurs reading {0} file, at line: \n {1} \n'.format(input_file, row))
        mapping.export_mappings(mapping_file)

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


def get_iso_time(time = datetime.datetime.now()):
    return "{0}Z/14".format(time.replace(microsecond=0).isoformat())

def progress(count, total, suffix=''):
	bar_len = 60
	filled_len = int(round(bar_len * count / float(total)))

	percents = round(100.0 * count / float(total), 1)
	bar = '=' * filled_len + '-' * (bar_len - filled_len)

	sys.stdout.write('[%s] %s%s %s Processing line: %s \r' % (bar, percents, '%', suffix, count))
	sys.stdout.flush()  

