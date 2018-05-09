import tests.domain_test as domain_test
import tests.business_test as business_test
import unittest
import domain.localizations as loc
import business.services.file_service as file_svc


def run_test(test_suite) :
    suite = unittest.TestLoader().loadTestsFromTestCase(test_suite)
    unittest.TextTestRunner(verbosity=2).run(suite)

# backup mappings
file_svc.backup(loc.known_mapping_file)
file_svc.backup(loc.unknown_mapping_file)
file_svc.fast_backup(loc.output_file)

run_test(business_test.QueriesTest)
run_test(business_test.UrlSvcTest)
run_test(business_test.QuickStatementSvcTest)
run_test(domain_test.MappingTest)
# run_test(business_test.TestOnTheFly)

# restore mappings
file_svc.restore(loc.known_mapping_file)
file_svc.restore(loc.unknown_mapping_file)
file_svc.fast_restore(loc.output_file)