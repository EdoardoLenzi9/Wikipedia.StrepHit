import tests.domain_test as domain_test
import tests.business_test as business_test
import unittest

def run_test(test_suite) :
    suite = unittest.TestLoader().loadTestsFromTestCase(test_suite)
    unittest.TextTestRunner(verbosity=2).run(suite)

run_test(domain_test.MappingTest)
run_test(business_test.QueriesTest)

run_test(business_test.UrlSvcTest)
run_test(business_test.QuickStatementSvcTest)
run_test(business_test.TestOnTheFly)


