import unittest
import business.utils.url_utils as url_utils
from business.mapping import LinkMapping, Mapping
import domain.localizations as loc
class MappingTest(unittest.TestCase):

    def test_add_new_source(self):
        # Arrange
        old_source =  LinkMapping("Q176251", "S2431", "http://www.museothyssen.org/en/thyssen/ficha_artista/$1")
        new_source =  LinkMapping("Q1762512345", "S2431", "http://www.museothyssen.org/en/thyssen/ficha_artista/$1")
        new_domain = "test"
        old_domain = "www.museothyssen.org"

        # Act
        mapping = Mapping(loc.source_mapping_file, loc.error_file)
        mapping.load(loc.source_mapping_file)
        mapping.add_domain(new_domain, new_source)
        mapping.add_domain(old_domain, new_source)
        mapping.add_domain(old_domain, old_source)

        # Assert
        self.assertEqual(mapping.get(new_domain)[0], new_source)
        self.assertEqual(mapping.get(old_domain)[0], old_source)
        self.assertEqual(mapping.get(old_domain)[1], new_source)
        self.assertEqual(len(mapping.get(old_domain)), 2)
