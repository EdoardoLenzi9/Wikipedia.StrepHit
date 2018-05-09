import business.services.quickstatements_service as quickstatements_svc
import business.services.file_service as file_svc
import domain.localizations as loc

print("Procedure started at: {0}".format(quickstatements_svc.get_iso_time()))

quickstatements_svc.refresh_urls(["www.bbc.co.uk"])

file_svc.rename(loc.input_file, loc.old_input_file)
file_svc.rename(loc.output_file, loc.input_file)

quickstatements_svc.add_db_references_async()
#quickstatements_svc.export_unmapped_url_list()
#quickstatements_svc.add_db_references_async(True)
#quickstatements_svc.add_db_references_async()

print("Procedure ended at: {0}".format(quickstatements_svc.get_iso_time()))