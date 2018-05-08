import business.services.quickstatements_service as quickstatements_svc

print("Procedure started at: {0}".format(quickstatements_svc.get_iso_time()))

#quickstatements_svc.export_unmapped_url_list()
#quickstatements_svc.add_db_references_async(True)
quickstatements_svc.add_db_references_async()

print("Procedure ended at: {0}".format(quickstatements_svc.get_iso_time()))