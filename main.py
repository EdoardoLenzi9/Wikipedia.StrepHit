import business.utils.quickstatememnts_utils as qs_utils
from business.services.quickstatements_service import QuickStatementsService
import business.utils.file_utils as file_utils
import domain.localizations as loc

quickStatementsService = QuickStatementsService()

def launch_method(name, method):
    print('start -> {0}\n'.format(name))
    print("Procedure started at: {0}\n".format(qs_utils.get_iso_time()))
    method()
    print("Procedure ended at: {0}\n".format(qs_utils.get_iso_time()))
    print('end -> {0}\n'.format(name))

def refresh():
    launch_method("Refresh urls", quickStatementsService.refresh_urls)

def add_references():
    launch_method("Add references", quickStatementsService.add_db_references_async())

def refresh_and_add():
    print("start -> Refresh urls and add references\n")
    print('start -> Refresh urls\n')
    print("Procedure started at: {0}\n".format(qs_utils.get_iso_time()))
    quickStatementsService.refresh_urls()
    print("Procedure ended at: {0}\n".format(qs_utils.get_iso_time()))
    print('end -> Refresh urls\n')    

    file_utils.rename(loc.input_file, loc.old_input_file)
    file_utils.rename(loc.output_file, loc.input_file)

    print('start -> Add references\n')
    print("Procedure started at: {0}\n".format(qs_utils.get_iso_time()))
    quickStatementsService.add_db_references_async()
    print("Procedure ended at: {0}\n".format(qs_utils.get_iso_time()))
    print('end -> Add references\n')    

def export_unmapped():
    launch_method("Export unmapped urls list", quickStatementsService.export_unmapped_url_list())

def refresh_urls_to_https():
    launch_method("Refresh urls to https", quickStatementsService.refresh_urls_to_https())

def refresh_urls_as_query_params():
    launch_method("Refresh urls as query params", quickStatementsService.refresh_urls_as_query_params())

# uncomment the procedure that you need:
# refresh_urls_as_query_params()
# refresh_urls_to_https()
# refresh()
# add_references()
# refresh_and_add()
# export_unmapped()