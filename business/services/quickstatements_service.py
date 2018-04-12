import os, datetime #, re re.match()
from domain.models.quick_statement import QuickStatement, Qualifier, Source, Command
import domain.mapping as mapping
import business.services.url_service as url_svc
 
def update_references (input_file, output_file, error_file):
    if not exists(input_file) :
        raise Exception("file: {0} not found".format(input_file))

    with open(input_file) as file:
        rows = file.readlines() 
        for row in rows:
            try:  
                sitelink = get_link(row)
                if sitelink != None :
                    reference = generate_db_reference(sitelink)
                    log(output_file, "{0}\t{1}".format(row, reference))
                else :
                    log(error_file, "No sitelink at line \t {0}".format(row))

            except :
                print('An error occurs reading {0} file, at line: \n {1} \n'.format(input_file, row))

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

def generate_db_reference(sitelink):
    domain = url_svc.get_domain(sitelink)
    try: 
        values = mapping.SOURCE_MAPPING[domain]
        #todo multiple link mappings
        link_mapping = values[0]
        if url_svc.validate_url_template(sitelink, link_mapping) : #todo case like more than $1
            url_pattern = link_mapping.url_pattern.split("$1")
            content = sitelink.replace(url_pattern[0], "").replace(url_pattern[1], "")
            return "S248\t{0}\t{1}\t{2}\tS813\t{3}".format(link_mapping.db_id, link_mapping.db_property, content, get_iso_time())
        else :            
            print('Fail validate template {0} \t {1}\n'.format(sitelink, link_mapping.url_pattern))
    except :
        print('URL not mapped: \n {1} \n'.format(sitelink))

def log(file, text):
    with open(file, 'ab+') as f:
            f.write("{0}\n".format(text))

def exists(file):
    return os.path.isfile(file)

def get_iso_time(time = datetime.datetime.now()):
    return "{0}Z/14".format(time.replace(microsecond=0).isoformat())
