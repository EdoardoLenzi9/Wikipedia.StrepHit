import business.services.quickstatements_service as quickstatements_svc
import json
import domain.mapping as mapping
#quickstatements_svc.parse("/home/eddy/Code/Wikipedia/Wikipedia.StrepHit/assets/supervised_dataset_reduced.qs")
#url_svc.get("https://www.wikidata.org/wiki/Special:EntityData/Q1373513.json");
#quickstatements_svc.update_references("/home/eddy/Code/Wikipedia/Wikipedia.StrepHit/assets/supervised_dataset_reduced.qs", "output.qs", "errors.log")

quickstatements_svc.update_references("/home/eddy/Code/Wikipedia/Wikipedia.StrepHit/assets/supervised_dataset.qs", "output.qs", "errors.log")

#TODO relative path .qs file
#TODO use lex and yacc

