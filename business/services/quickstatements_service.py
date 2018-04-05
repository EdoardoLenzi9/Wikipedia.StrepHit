import os, datetime
from domain.models.quick_statement import QuickStatement, Qualifier, Source, Command

def parse (file_path):
    if not exists(file_path) :
        raise Exception("file: {0} not found".format(file_path))

    quickstatements = []
    with open(file_path) as file:
        rows = file.readlines() 
        for row in rows:
            row = row.strip()               # take out leading and ending spaces
            directives = [x.strip() for x in row.split('\t')]
            try:           
                current_statement = QuickStatement(directives[0], directives[1], directives[2], [], [], [], [], [], [])
                '''
                index = 2
                while (index < len(directives) -1):
                    index += 1
                    key = directives[index]
                    index += 1
                    value = directives[index]
                    first_char = key[0]
                    if first_char == "P": 
                        current_statement.qualifiers.append(Qualifier(key, value))
                    elif first_char == "S": 
                        current_statement.sources.append(Source(key, value))
                    elif first_char == "L": 
                        current_statement.labels.append(Command(key, value))
                    elif first_char == "A": 
                        current_statement.aliases.append(Command(key, value))
                    elif first_char == "D": 
                        current_statement.descriptions.append(Command(key, value)) 
                    elif first_char == "S": 
                        current_statement.sitelinks.append(Command(key, value)) 
                    '''
                quickstatements.append(current_statement)
            except :
                print('An error occurs reading {0} file, at line: \n {1} \n'.format(file_path, row))
    return quickstatements

def exists(file):
    return os.path.isfile(file)

def get_iso_time(time = datetime.datetime.now()):
    return "{0}Z/14".format(time.replace(microsecond=0).isoformat())

def append_db_reference(quickstatement):
    