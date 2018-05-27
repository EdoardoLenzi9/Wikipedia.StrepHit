import re, time, sys, threading
import domain.localizations as loc
import business.utils.url_utils as url_utils
import business.queries.sitelink_queries as query
import business.utils.file_utils as file_utils
import business.utils.quickstatememnts_utils as qs_utils
from business.mapping import Mapping, LinkMapping
from business.quickstatement import QuickStatement


class QuickStatementsService(object):

    def __init__(self):
        self.__total = 0
        self.__index = 0
        self.__mappings = Mapping(loc.mapping_file, loc.error_file)
        self.__unknown_mappings = Mapping(loc.unknown_mapping_file, loc.error_file)
        self.__refreshed_urls = {}
        self.domains = []
        self.domains_just_mapped = []
        self.__mappings.load(loc.source_mapping_file)
        if loc.LOAD_MAPPINGS:
            self.__mappings.load(loc.source_mapping_file)
            self.__mappings.load()
            self.__unknown_mappings.load()
            if loc.REFRESH_UNKNOWN_DOMAINS :
                self.domains = self.__unknown_mappings.get_domains()

    # testing
    def get_mappings(self, domain):
        return self.__mappings.get(domain)
    
    def get_unknown_mappings(self, domain):
        return self.__unknown_mappings.get(domain)

    # wrappers
    def refresh_urls (self, domains = loc.domains_to_refresh):
        for domain in domains:
            if domain not in self.domains:
                self.domains.append(domain)

        self. __rows_cycle(self.__refresh_urls_handler)

    def export_unmapped_url_list (self):
        self. __rows_cycle(self.__export_unmapped_url_list_handler)

    def add_db_references_async (self):
        self. __rows_cycle(self.__add_db_references_async_handler)   

    def generate_db_reference_wrapper(self, qs):  
        reference = self.generate_db_reference(qs)
        qs.append(reference)
        file_utils.log(loc.output_file, qs.serialize())
        self.__export_mappings()
        self.__progress()

    def generate_db_reference(self, qs):
        if(qs.domain is None):
            return qs_utils.db_reference()
        if(self.is_unknown_source(qs)) :
            return self.__get_db_id(qs.domain)
        try: 
            for link_mapping in self.__mappings.get(qs.domain) :
                if url_utils.validate_url_template(qs.sitelink, link_mapping.url_pattern) : 
                    content = url_utils.extract_placeholder(link_mapping, qs.sitelink)
                    return qs_utils.db_reference(link_mapping, content)
            if(loc.MAP_ALL_RESPONSES and self.__is_domain_just_mapped(qs)) :
                return self.__get_db_id(qs.domain)
            raise Exception("mapping not found")
        except : 
            if loc.MAP_ALL_RESPONSES:
                return self.__mapping_all(qs)
            return self.__new_mapping(qs)

    def __rows_cycle(self, handler):
        if not file_utils.exists(loc.input_file) :
            raise Exception("file: {0} not found".format(loc.input_file))
        with open(loc.input_file) as file:
            rows = file.readlines() 
            self.total = len(rows)
            self.index = 0
            for row in rows:
                try :
                    qs = QuickStatement(row) 
                    handler(qs)
                except : 
                    file_utils.log(loc.error_file, "Error at row: {0}".format(row))

    # handlers
    def __refresh_urls_handler(self, qs): 
        self.__progress()
        old_sitelink = qs.sitelink
        if qs.sitelink is not None :
            if self.__refreshed_urls.get(qs.sitelink) is not None :
                qs.set_sitelink(self.__refreshed_urls.get(qs.sitelink))
            elif len(self.domains) == 0 or (qs.domain in self.domains):
                if qs.refresh():
                    self.__refreshed_urls[old_sitelink] = qs.sitelink
                    file_utils.export(loc.refreshed_urls_file, self.__refreshed_urls)
                elif loc.DELETE_ROW and qs.sitelink is None:
                    qs.delete_sitelink()
                    file_utils.log(loc.deleted_rows_file, "{0} \t old_link \t {1}".format(qs.serialize(), old_sitelink))
                    return
            file_utils.log(loc.output_file, qs.serialize())
 
    def __export_unmapped_url_list_handler(self, qs):
        self.__progress()
        if qs.sitelink is not None :
            is_not_mapped = True
            for link_mapping in self.__mappings.get(qs.domain):
                if qs.validate(link_mapping.url_pattern):
                    is_not_mapped = False
            if is_not_mapped :
                file_utils.log(loc.output_file, qs.sitelink)

    def __add_db_references_async_handler(self, qs):
        if qs.sitelink is not None :
            if(loc.IS_ASYNC_MODE):
                thread = threading.Thread(target=self.generate_db_reference_wrapper, args=(qs))
                thread.daemon = True
                thread.start()                       
            else :
                self.generate_db_reference_wrapper(qs)

    def __new_mapping(self, qs): 
        db_id = None
        try:
            result = query.get_item(qs.domain) 

            if len(result) != 0 :
                if len(result) == 1:
                    row = result[0]
                    if not hasattr(row, 'formatterUrlLabel') and hasattr(row, 'sitelinkLabel'):
                        domain = url_utils.get_domain(row.sitelinkLabel.value)
                        self.__unknown_mappings.add_domain(domain, domain)
                        self.__mappings.add_domain(domain, domain)
                        return self.__get_db_id(domain)
                for row in result :
                    db_id = qs_utils.get_identifier(row.subjects.value, "Q")
                    if hasattr(row, 'wikidataProperty') and hasattr(row, 'formatterUrlLabel') and hasattr(row, 'sitelinkLabel'):
                        real_domain = url_utils.get_domain(row.sitelinkLabel.value)
                        db_property = qs_utils.get_identifier(row.wikidataProperty.value, "P").replace("P", "S") 
                        url_pattern = row.formatterUrlLabel.value
                        if url_utils.validate_url_template(qs.sitelink, url_pattern) : 
                            pattern = url_pattern.split("$1")
                            content = qs.sitelink.replace(pattern[0], "").replace(pattern[1], "")
                            self.__mappings.add_domain(real_domain, LinkMapping(db_id, db_property, url_pattern))
                            return qs_utils.db_reference(LinkMapping(db_id, db_property), content)
            else:
                self.__unknown_mappings.add_domain(qs.domain, qs.domain)
                return qs_utils.db_reference()
            raise Exception("db domain not found in wikidata")
        except : 
            regex = re.compile("{0}/[^/]+".format(qs.domain))
            uri = regex.search(qs.sitelink).group(0)  
            while uri != "" :
                result = query.get_item(uri)
                if len(result) == 0 :
                    self.__unknown_mappings.add_domain(qs.domain, uri)
                    self.__mappings.add_domain(qs.domain, LinkMapping(db_id))
                    break
                regex = re.compile("{0}/[^/]+".format(uri))
                uri = regex.search(qs.sitelink).group(0)  
            return self.__get_db_id(qs.domain)

    def __mapping_all(self, qs): 
        self.domains_just_mapped.append(qs.domain)
        db_id = None
        try:
            result = query.get_item(qs.domain) 

            for row in result :
                real_domain = url_utils.get_domain(row.sitelinkLabel.value)
                db_id = qs_utils.get_identifier(row.subjects.value, "Q")
                db_property =  qs_utils.get_identifier(row.wikidataProperty.value, "P").replace("P", "S") if hasattr(row, 'wikidataProperty') else None
                url_pattern = row.formatterUrlLabel.value if  hasattr(row, 'formatterUrlLabel') else None 
                self.__mappings.add_domain(real_domain, LinkMapping(db_id, db_property, url_pattern))

            for link_mapping in self.__mappings.get(qs.domain) :
                if url_utils.validate_url_template(qs.sitelink, link_mapping.url_pattern) : 
                    content = url_utils.extract_placeholder(link_mapping, qs.sitelink)
                    return qs_utils.db_reference(link_mapping, content)

            if len(result) == 0:
                self.__unknown_mappings.add_domain(qs.domain, qs.domain)
                return qs_utils.db_reference()
            raise Exception("db domain not found in wikidata")
        except : 
            regex = re.compile("{0}/[^/]+".format(qs.domain))
            uri = regex.search(qs.sitelink).group(0)  
            while uri != "" :
                result = query.get_item(uri)
                if len(result) == 0 :
                    self.__unknown_mappings.add_domain(qs.domain, uri)
                    self.__mappings.add_domain(qs.domain, LinkMapping(db_id))
                    break
                regex = re.compile("{0}/[^/]+".format(uri))
                uri = regex.search(qs.sitelink).group(0)  
            return self.__get_db_id(qs.domain)

    def __export_mappings(self):
        self.__mappings.save()
        self.__unknown_mappings.save()

    def __progress(self, suffix=''):
        self.index += 1
        bar_len = 60
        filled_len = int(round(bar_len * self.index / float(self.total)))

        percents = round(100.0 * self.index / float(self.total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)
        try:
            sys.stdout.write('[%s] %s%s %s Processing line: %s \r' % (bar, percents, '%', suffix, self.index))
            sys.stdout.flush()  
        except :
            print ("\n warning: [shuld never happen error] loader-bar error count \t {0} \t total {1} \n".format(self.index, self.total))

    def is_unknown_source(self, qs):
        if self.__unknown_mappings.get(qs.domain) is not None : 
            for unknown_source in self.__unknown_mappings.get(qs.domain):
                if unknown_source in qs.sitelink: 
                    return True
        return False 

    def __get_db_id(self, domain):
        for mapping_entry in self.__mappings.get(domain) :
            if mapping_entry.db_id is not None :
                return qs_utils.db_reference(LinkMapping(db_id=mapping_entry.db_id))
        return qs_utils.db_reference()

    def __is_domain_just_mapped(self, qs):
        if qs.domain not in self.domains_just_mapped : 
            return True
        return False 