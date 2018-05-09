import unittest, re
import business.queries.sitelink_queries as query
import business.services.quickstatements_service as qs_svc
import business.services.url_service as url_svc
import domain.localizations as loc
import domain.mapping as mapping

class QueriesTest(unittest.TestCase):
    
    def test_sparql_query(self):
        # Arrange and Act
        result = query.get_item("nndb")

        # Assert
        self.assertEqual(len(result), 2) # TODO improve this test because, in future, this value will change...

class UrlSvcTest(unittest.TestCase):
    
    def test_validate_url_template(self):
        # Arrange
        sitelink = "http://sculpture.gla.ac.uk/view/person.php?id=msib3_1266502314"
        url_pattern = "http://sculpture.gla.ac.uk/view/person.php?id=$1"

        # Act and Assert
        self.assertTrue(url_svc.validate_url_template (sitelink, url_pattern))

    def test_get_domain(self):
        # Arrange
        sitelink = "https://en.wikisource.org/"

        # Act and Assert
        self.assertEqual(url_svc.get_domain(sitelink), "en.wikisource.org")

    def test_import_mappings(self):
        # Act and Assert
        mapping.import_mappings();
        
        self.assertEqual(0,0) #TODO
    
    def test_url_refresh_on_a_changed_url(self):
        # Arrange
        old_url = 'https://www.bbc.co.uk/arts/yourpaintings/artists/cornelis-troost'
        new_url = 'https://artuk.org/discover/artists/troost-cornelis-16961750'

        # Act 
        refreshed_url = url_svc.refresh_url(old_url)
        
        # Assert
        self.assertEqual(refreshed_url, new_url)

    def test_url_refresh_on_an_inexistent_url(self):
        # Arrange
        old_url = 'https://www.thisurlnotexistsihope.com'

        # Act 
        refreshed_url = url_svc.refresh_url(old_url)
        
        # Assert
        self.assertIsNone(refreshed_url)

    def test_url_refresh_on_an_normal_url(self):
        # Arrange
        url = 'http://adb.anu.edu.au/biography/white-patrick-victor-paddy-14925'

        # Act 
        refreshed_url = url_svc.refresh_url(url)
        
        # Assert
        self.assertEqual(refreshed_url, url)

class QuickStatementSvcTest(unittest.TestCase):

    def test_generate_db_reference_for_an_unknown_domain(self):
        # Arrange         
        link =  "http://sculpture.gla.ac.uk/view/person.php?id=msib3_1266502314"

        # Act
        reference = qs_svc.generate_db_reference(link)

        # Assert
        domain = url_svc.get_domain(link)
        self.assertTrue(mapping.SOURCE_MAPPING.get(domain))
        self.assertEqual(mapping.SOURCE_MAPPING[domain][0].url_pattern, "http://sculpture.gla.ac.uk/view/person.php?id=$1")
        self.assertIn("S248\tQ6754185\tS2914\t", reference)

    def test_generate_db_reference_for_a_known_domain(self):
        # Arrange         
        # "adb.anu.edu.au": [ LinkMapping("Q672680", "S1907", "http://adb.anu.edu.au/biography/$1") ]
        link = "http://adb.anu.edu.au/biography/gregory-henry-6477"
        
        # Act
        reference = qs_svc.generate_db_reference(link)

        # Assert
        domain = url_svc.get_domain(link)
        mapping_list = mapping.SOURCE_MAPPING[domain] 
        for mapping_entry in mapping_list :
            if url_svc.validate_url_template(link, mapping_entry.url_pattern) : 
                content = url_svc.extract_placeholder(mapping_entry.url_pattern, link)
        reference_prefix = "S248\t{0}\t{1}\t\"{2}\"\tS813\t".format(mapping_entry.db_id, mapping_entry.db_property, content)

        self.assertIn(reference_prefix, reference)
        
    def test_generate_db_reference_for_a_known_domain_but_unknown_url_pattern(self):
        # Arrange         
        link =  "https://archive.org/download/biographicaldict01johnuoft/biographicaldict01johnuoft_djvu.txt"

        # Act
        reference = qs_svc.generate_db_reference(link)

        # Assert
        domain = url_svc.get_domain(link)
        self.assertTrue(qs_svc.is_unknown_source(domain, link))
        self.assertIn("S248\tQ461\tS813\t", reference)
        self.assertIn("archive.org/download", mapping.UNKNOWN_SOURCE_MAPPING[domain])

    def test_generate_db_reference_for_an_unknown_domain_for_wikidata(self):
        # Arrange         
        link = "https://www.daao.org.au/bio/watts/"

        # Act
        reference = qs_svc.generate_db_reference(link)

        # Assert
        domain = url_svc.get_domain(link)
        self.assertTrue(qs_svc.is_unknown_source(domain, link))
        self.assertEqual("", reference)
        self.assertIn("www.daao.org.au", mapping.UNKNOWN_SOURCE_MAPPING[domain])
'''
class TestOnTheFly(unittest.TestCase):
    def test_generate_db_reference_with_url_similar_to_a_wikidata_url_pattern(self):
        # Arrange         
        link = "http://vocab.getty.edu/ulan/500122964"

        # Act
        reference = qs_svc.generate_db_reference(link)

        # Assert
        domain = url_svc.get_domain(link)
        self.assertTrue(True) # TODO implement test
'''