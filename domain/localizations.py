# Link
sparql_url = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"
entity_url = "https://www.wikidata.org/wiki/Special:EntityData/"

# File
old_input_file = "assets/supervised_dataset_old.qs"
input_file = "assets/supervised_dataset.qs"
test_file = "assets/supervised_dataset_reduced.qs"
output_file = "assets/supervised_dataset_output.qs"
error_file =  "assets/supervised_dataset_errors.log"

source_mapping_file = "assets/supervised_dataset_source_mappings.json"
mapping_file = "assets/supervised_dataset_mappings.json"
unknown_mapping_file = "assets/supervised_dataset_unknown_mappings.json"
refreshed_urls_file = "assets/supervised_dataset_refreshed_urls.json"

# Const
LOAD_MAPPINGS = True
MAP_ALL_RESPONSES = False
IS_ASYNC_MODE = False
DELETE_ROW = False # delete row when refresh url which is not reachable (must have stable internet connection)
REFRESH_UNKNOWN_DOMAINS = True

