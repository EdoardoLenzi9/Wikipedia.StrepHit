import business.utils.file_utils as file_utils
import business.utils.url_utils as url_utils
import domain.localizations as loc 

class QuickStatement(object):
    domain = None
    sitelink = None
    __serialized_object = None

    def __init__(self, serialized_object = None, link = None):
        if serialized_object is not None:
            self.__serialized_object = serialized_object.replace("\n", "")
            self.sitelink = url_utils.get_link(serialized_object)
            if self.sitelink is None:
                file_utils.log(loc.error_file, "No sitelink at line \t {0}".format(serialized_object))
            self.domain = url_utils.get_domain(self.sitelink)
            if self.domain is None:
                file_utils.log(loc.error_file, "No domain at line \t {0}".format(serialized_object))
        if link is not None:
            self.set_sitelink(link)

    def refresh(self):
        refreshed_url = url_utils.refresh_url(self.sitelink)
        self.set_sitelink(refreshed_url)
        if refreshed_url is not None and refreshed_url != self.sitelink:
            return True
        return False
    
    def serialize(self):
        return self.__serialized_object

    def set_sitelink(self, sitelink):
        if self.__serialized_object is not None :
            self.__serialized_object = self.__serialized_object.replace(self.sitelink, sitelink)
        self.sitelink = sitelink
        self.domain = url_utils.get_domain(sitelink)

    def delete_sitelink(self):
        self.__serialized_object = self.__serialized_object.replace("S854\t{0}".format(self.sitelink), "")
        self.sitelink = None
        self.domain = None
    
    def validate(self, template):
        return url_utils.validate_url_template(self.sitelink, template) 

    def append(self, reference):
        self.__serialized_object = "{0}\t{1}".format(self.__serialized_object, reference)