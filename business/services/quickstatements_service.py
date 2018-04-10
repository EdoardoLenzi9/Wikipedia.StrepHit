import os, datetime #, re re.match()
from domain.models.quick_statement import QuickStatement, Qualifier, Source, Command
import domain.mapping as mapping
import business.services.url_service as url_svc

def parse (row):
    content = [x.strip() for x in row.strip().split('\t')]
    current_statement = QuickStatement(content[0], content[1], content[2], [], [], [], [], [], [])
    
    index = 2
    while (index < len(content) -1):
        index += 1
        key = content[index]
        index += 1
        value = content[index]
        
        if(key == "S854"): # "Reference URL"
            current_statement.sitelinks.append(Command(key, value))
        if(key == "S248"): # "stated in"
            current_statement.sources.append(Command(key, value))
    return current_statement

def update_references (input_file, output_file):
    if not exists(input_file) :
        raise Exception("file: {0} not found".format(input_file))

    with open(input_file) as file:
        rows = file.readlines() 
        for row in rows:
            try:  
                current_statement = parse(row)
                reference = db_reference(current_statement)
                log(output_file, "{0}\t{1}".format(row, reference))
            except :
                print('An error occurs reading {0} file, at line: \n {1} \n'.format(input_file, row))

def log(file, text):
    with open(file, 'ab+') as f:
            f.write("{0}\n".format(text))

def exists(file):
    return os.path.isfile(file)

def get_iso_time(time = datetime.datetime.now()):
    return "{0}Z/14".format(time.replace(microsecond=0).isoformat())

def db_reference(quickstatement):
    if(len(quickstatement.sitelinks) > 0): #TODO multiple url
        domain = url_svc.get_domain(quickstatement.sitelinks[0].content)
        try: 
            key = mapping.SOURCE_MAPPING[domain]
            print(key)
            return "S248\t{1}\t{2}S1263\t{3}"702/000094420"\t{4}S813\t{5}+2018-03-22T00:00:00Z/11".format(key[0])
        except :
            print('URL not mapped: \n {1} \n'.format(quickstatement.sitelinks[0].content))
    else :
        print('Statement not contains any sitelink: \n {1} \n'.format(quickstatement.item))
        return ""