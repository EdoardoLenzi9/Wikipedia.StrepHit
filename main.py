import business.utils.quickstatememnts_utils as qs_utils
from business.services.quickstatements_service import QuickStatementsService

import business.utils.file_utils as file_utils
import domain.localizations as loc


print("Procedure started at: {0}".format(qs_utils.get_iso_time()))
quickStatementsService = QuickStatementsService()

quickStatementsService.refresh_urls()

file_utils.rename(loc.input_file, loc.old_input_file)
file_utils.rename(loc.output_file, loc.input_file)

#quickStatementsService.add_db_references_async()
#quickstatements_svc.export_unmapped_url_list()
#quickstatements_svc.add_db_references_async(True)
#quickstatements_svc.add_db_references_async()

print("Procedure ended at: {0}".format(qs_utils.get_iso_time()))