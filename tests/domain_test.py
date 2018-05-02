import unittest
import domain.mapping as mapping

class MappingTest(unittest.TestCase):
    
    def test_add_new_source(self):
        # Arrange
        old_source =  mapping.LinkMapping("Q672680", "S1907", "http://adb.anu.edu.au/biography/$1")
        new_source =  mapping.LinkMapping("Q6726801", "S1907", "http://adb.anu.edu.au/biography/$1")
        new_domain = "test"
        old_domain = "adb.anu.edu.au"

        # Act
        mapping.add_source(new_domain, new_source)
        mapping.add_source(old_domain, new_source)
        mapping.add_source(old_domain, old_source)

        # Assert
        self.assertEqual(mapping.SOURCE_MAPPING[new_domain][0], new_source)
        self.assertEqual(mapping.SOURCE_MAPPING[old_domain][1], new_source)
        self.assertRaises(mapping.SOURCE_MAPPING[old_domain][2])
     