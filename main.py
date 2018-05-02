import business.services.quickstatements_service as quickstatements_svc

input_file = "assets/supervised_dataset.qs"
output_file = "assets/supervised_dataset_output.qs"
log_file =  "assets/supervised_dataset_errors.log"
known_mapping_file = "assets/supervised_dataset_mappings.json"
unknown_mapping_file = "assets/supervised_dataset_unknown_mappings.json"
not_mapped_url = "assets/not_mapped_url.txt"

print("Procedure started at: {0}".format(quickstatements_svc.get_iso_time()))

#quickstatements_svc.export_unmapped_url_list(input_file, not_mapped_url)
quickstatements_svc.update_references(input_file, output_file, log_file, known_mapping_file)

print("Procedure ended at: {0}".format(quickstatements_svc.get_iso_time()))