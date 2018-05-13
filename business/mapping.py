import json
import business.utils.file_utils as file_utils
import business.utils.url_utils as url_utils
import domain.localizations as loc 

class LinkMapping(object):
    db_id = None
    db_property = None
    url_pattern = None
    
    def __eq__(self, other):
        if self.db_id == other.db_id and self.db_property == other.db_property and self.url_pattern == other.url_pattern :
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __init__(self, db_id = None, db_property = None, url_pattern = None):
        self.db_id = db_id
        self.db_property = db_property
        if url_pattern != None :
            url_pattern = url_pattern.encode('ascii')
        self.url_pattern = url_pattern

class Mapping(object) :
    # dictionary (key : value = [])
    __content = {} 
    __file = "" 
    __log_file = ""

    def __init__(self, file, log_file):
        self.__content = {}
        self.__file = file
        self.__log_file = log_file
    
    def add(self, key, value, export=True):
        if self.__content.get(key) == None : 
            self.__content[key] = [value]
        elif value not in self.__content[key]:                         
            self.__content[key].append(value)
        if export:
            self.save()
    
    def add_domain(self, key, value, export=True):
        if key != None :
            key.encode('ascii').replace("/", "")
        self.add(key, value, export)

    def save(self, mode = 'w'):
        serialized_object = json.dumps(self.__content, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        file_utils.log(self.__file, serialized_object, mode)

    def load(self, source_file = None):
        if source_file is None :
            source_file = self.__file
        try :
            with open(source_file) as file:
                items = json.load(file)
                for item in items :
                    for subitem in items[item] :
                        if isinstance(subitem, dict) :
                            link_mapping = LinkMapping(subitem["db_id"], subitem["db_property"], subitem["url_pattern"])  
                            self.add(item, link_mapping, False)
                        elif isinstance(subitem, basestring) :
                            self.add(item, subitem, False)
        except :
            file_utils.log(self.__log_file, "Error, wrong mapping files: {0} \n".format(self.__file)) 

    def get_domains(self):
        domains = self.__content.keys()
        if domains is None :
            return []
        return self.__content.keys()

    def get(self, item):
        if item != None and self.contains(item):
            return self.__content[item]
        return []

    def contains(self, item):
        return self.__content.get(item) != None
