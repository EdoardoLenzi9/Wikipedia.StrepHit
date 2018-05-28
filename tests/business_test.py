import unittest, re
import business.queries.sitelink_queries as query
import business.services.quickstatements_service as qs_svc
import business.utils.url_utils as url_utils
import domain.localizations as loc
from business.services.quickstatements_service import QuickStatementsService 
from business.quickstatement import QuickStatement
import business.utils.quickstatememnts_utils as qs_utils 
from business.mapping import LinkMapping

class QueriesTest(unittest.TestCase):
    
    def test_sparql_query(self):
        # Arrange and Act
        result = query.get_item("nndb")

        # Assert
        self.assertEqual(len(result), 2) # TODO improve this test because, in future, this value will change...

class UrlSvcTest(unittest.TestCase):
    
    def test_bug_on_url_refresh(self):
        # Arrange
        # url = 'http://vocab.getty.edu/ulan/500122964'
        url = 'http://vocab.getty.edu/ulan/500122964'

        # Act 
        refreshed_url = url_utils.refresh_url(url)
        
        # Assert
        self.assertEqual(refreshed_url, url)

    def test_build_query_url(self):
        # Arrange
        base_url = "https://collection.britishmuseum.org/resource/"
        query = {"uri" : "http://collection.britishmuseum.org/id/person-institution/143629"}
        url = url_utils.build_query_url(base_url, query);
        self.assertEqual(url, "https://collection.britishmuseum.org/resource/?uri=http%3A%2F%2Fcollection.britishmuseum.org%2Fid%2Fperson-institution%2F143629")

    def test_validate_url_template(self):
        # Arrange
        sitelink = "http://sculpture.gla.ac.uk/view/person.php?id=msib3_1266502314"
        url_pattern = "http://sculpture.gla.ac.uk/view/person.php?id=$1"

        # Act and Assert
        self.assertTrue(url_utils.validate_url_template (sitelink, url_pattern))

    def test_get_domain(self):
        # Arrange
        sitelink = "https://en.wikisource.org/"

        # Act and Assert
        self.assertEqual(url_utils.get_domain(sitelink), "en.wikisource.org")

    def test_import_mappings(self):
        # Act and Assert
        qs_svc = QuickStatementsService()
        
        self.assertEqual(0,0) #TODO
    
    def test_url_refresh_on_a_changed_url(self):
        # Arrange
        old_url = 'https://www.bbc.co.uk/arts/yourpaintings/artists/cornelis-troost'
        new_url = 'https://artuk.org/discover/artists/troost-cornelis-16961750'

        # Act 
        refreshed_url = url_utils.refresh_url(old_url)
        
        # Assert
        self.assertEqual(refreshed_url, new_url)

    def test_url_refresh_on_an_inexistent_url(self):
        # Arrange
        old_url = 'https://www.thisurlnotexistsihope.com'

        # Act 
        refreshed_url = url_utils.refresh_url(old_url)
        
        # Assert
        self.assertIsNone(refreshed_url)

    def test_url_refresh_on_a_normal_url(self):
        # Arrange
        url = 'http://adb.anu.edu.au/biography/white-patrick-victor-paddy-14925'

        # Act 
        refreshed_url = url_utils.refresh_url(url)
        
        # Assert
        self.assertEqual(refreshed_url, url)

    def test_url_extract_placeholder(self):
        # Arrange
        url = 'http://www.wga.hu/bio/j/joseph/biograph.html'
        formatter_url = "http://www.wga.hu/bio/j/$1/biograph.html"
        link_mapping = LinkMapping(0, 0, formatter_url, True)  
        # Act 
        placeholder = url_utils.extract_placeholder(link_mapping, url)
        
        # Assert
        self.assertEqual("JOSEPH", placeholder)

class QuickStatementSvcTest(unittest.TestCase):
    def test_generate_db_reference_for_an_unknown_domain(self):
        # Arrange    
        link =  "http://sculpture.gla.ac.uk/view/person.php?id=msib3_1266502314"
        loc.LOAD_MAPPINGS = False
        qs_svc = QuickStatementsService()   
        qs = QuickStatement(link=link)
        
        # Act
        reference = qs_svc.generate_db_reference(qs)

        # Assert
        self.assertTrue(qs_svc.get_mappings(qs.domain) != [])
        self.assertEqual(qs_svc.get_mappings(qs.domain)[0].url_pattern, "http://sculpture.gla.ac.uk/view/person.php?id=$1")
        self.assertIn("S248\tQ6754185\tS2914\t", reference)

    def test_generate_db_reference_for_a_known_domain(self):
        # Arrange         
        # "adb.anu.edu.au": [ LinkMapping("Q672680", "S1907", "http://adb.anu.edu.au/biography/$1") ]
        link = "http://adb.anu.edu.au/biography/gregory-henry-6477"
        loc.LOAD_MAPPINGS = False
        qs_svc = QuickStatementsService()   
        qs = QuickStatement(link=link)

        # Act
        reference = qs_svc.generate_db_reference(qs)

        # Assert
        domain = url_utils.get_domain(link)
        mapping_list = qs_svc.get_mappings(domain) 
        for mapping_entry in mapping_list :
            if url_utils.validate_url_template(link, mapping_entry.url_pattern) : 
                content = url_utils.extract_placeholder(mapping_entry, link)
        reference_prefix = "S248\t{0}\t{1}\t\"{2}\"\tS813\t".format(mapping_entry.db_id, mapping_entry.db_property, content)

        self.assertIn(reference_prefix, reference)

    def test_generate_db_reference_for_a_known_domain_but_unknown_url_pattern(self):
        # Arrange         
        link =  "https://archive.org/download/biographicaldict01johnuoft/biographicaldict01johnuoft_djvu.txt"
        loc.LOAD_MAPPINGS = False
        qs_svc = QuickStatementsService()   
        qs = QuickStatement(link=link)

        # Act
        reference = qs_svc.generate_db_reference(qs)

        # Assert
        self.assertTrue(qs_svc.is_unknown_source(qs))
        self.assertIn("S248\tQ461\tS813\t", reference)
        self.assertIn("archive.org/download", qs_svc.get_unknown_mappings(qs.domain))

    def test_generate_db_reference_for_an_unknown_domain_for_wikidata(self):
        # Arrange         
        link = "https://www.thisdomainnotexists.org.au/bio/watts/"
        loc.LOAD_MAPPINGS = False
        qs_svc = QuickStatementsService()   
        qs = QuickStatement(link=link)

        # Act
        reference = qs_svc.generate_db_reference(qs)

        # Assert
        domain = url_utils.get_domain(link)
        self.assertTrue(qs_svc.is_unknown_source(qs))
        self.assertEqual(qs_utils.db_reference(), reference)
        self.assertIn(qs.domain, qs_svc.get_unknown_mappings(domain))
'''
class TestOnTheFly(unittest.TestCase):
    def test_generate_db_reference_with_url_similar_to_a_wikidata_url_pattern(self):
        # Arrange         
        link = "http://vocab.getty.edu/ulan/500122964"

        # Act
        reference = qs_svc.generate_db_reference(qs)

        # Assert
        domain = url_utils.get_domain(link)
        self.assertTrue(True) # TODO implement test

    def test_generate_db_reference_with_arbitrary_url_pattern(self):
        # Arrange         
        link = "https://artuk.org/discover/artists/troost-cornelis-16961750"

        # Act
        domain = url_utils.get_domain(link)
        reference = qs_svc.generate_db_reference(qs)

        # Assert
        self.assertTrue(True) # TODO implement test
'''