sparql_url = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"
entity_url = "https://www.wikidata.org/wiki/Special:EntityData/"

input_file = "assets/supervised_dataset.qs"
test_file = "assets/supervised_dataset_reduced.qs"
output_file = "assets/supervised_dataset_output.qs"
error_file =  "assets/supervised_dataset_errors.log"
log_file = "assets/supervised_dataset.log"
known_mapping_file = "assets/supervised_dataset_mappings.json"
unknown_mapping_file = "assets/supervised_dataset_unknown_mappings.json"
not_mapped_url_file = "assets/not_mapped_url.txt"
old_input_file = "assets/supervised_dataset.old.qs"

# Const
MAP_ALL_RESPONSES = False
IS_ASYNC_MODE = False
DELETE_ROW = False # delete row when refresh url which is not reachable (must have stable internet connection)