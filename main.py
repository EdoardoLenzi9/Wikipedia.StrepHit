import business.services.quickstatements_service as quickstatements_svc

input_file = "assets/supervised_dataset.qs"
output_file = "assets/supervised_dataset_output.qs"
log_file =  "assets/supervised_dataset_errors.log"
mapping_file = "assets/supervised_dataset_mappings.json"
quickstatements_svc.update_references(input_file, output_file, log_file, mapping_file)


