import business.services.quickstatements_service as quickstatements_svc
import business.services.url_service as url_svc
#quickstatements_svc.parse("/home/eddy/Code/Wikipedia/Wikipedia.StrepHit/assets/supervised_dataset_reduced.qs")
#url_svc.get("https://www.wikidata.org/wiki/Special:EntityData/Q1373513.json");
quickstatements_svc.update_references("/home/eddy/Code/Wikipedia/Wikipedia.StrepHit/assets/supervised_dataset.qs", "output.qs")

#TODO relative path .qs file
#TODO use lex and yacc

