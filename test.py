import tests.domain_test as domain_test
import tests.business_test as business_test
import tests.output_test as output_test
import unittest
import domain.localizations as loc
import business.utils.file_utils as file_utils


def run_test(test_suite) :
    suite = unittest.TestLoader().loadTestsFromTestCase(test_suite)
    unittest.TextTestRunner(verbosity=2).run(suite)

# backup mappings
file_utils.backup(loc.mapping_file)
file_utils.backup(loc.unknown_mapping_file)
file_utils.fast_backup(loc.output_file)

run_test(output_test.OutputTest)
run_test(business_test.QuickStatementSvcTest)
run_test(business_test.QueriesTest)
run_test(business_test.UrlSvcTest)
run_test(domain_test.MappingTest)

#run_test(business_test.TestOnTheFly)

# restore mappings
file_utils.restore(loc.mapping_file)
file_utils.restore(loc.unknown_mapping_file)
file_utils.fast_restore(loc.output_file)