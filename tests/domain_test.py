import unittest
import domain.mapping as mapping
import business.services.url_service as url_svc
class MappingTest(unittest.TestCase):
    
    def test_add_new_source(self):
        # Arrange
        old_source =  mapping.LinkMapping("Q176251", "S2431", "http://www.museothyssen.org/en/thyssen/ficha_artista/$1")
        new_source =  mapping.LinkMapping("Q1762512345", "S2431", "http://www.museothyssen.org/en/thyssen/ficha_artista/$1")
        new_domain = "test"
        old_domain = "www.museothyssen.org"

        # Act
        mapping.add_source(new_domain, new_source)
        mapping.add_source(old_domain, new_source)
        mapping.add_source(old_domain, old_source)

        # Assert
        self.assertEqual(mapping.SOURCE_MAPPING[new_domain][0], new_source)
        self.assertEqual(mapping.SOURCE_MAPPING[old_domain][0], old_source)
        self.assertEqual(mapping.SOURCE_MAPPING[old_domain][1], new_source)
        self.assertEqual(len(mapping.SOURCE_MAPPING[old_domain]), 2)
