import business.services.url_service as url_svc
import re

def get_item(domain):
    #select Distinct ?subjects ?subjectsLabel ?sitelink ?sitelinkLabel ?wikidataProperty ?wikidataPropertyLabel ?formatterUrlLabel
    query = '''
        select Distinct ?subjects ?wikidataProperty ?formatterUrlLabel
        where {
            {
                BIND("{0}" AS ?domain).
                SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                ?subjects wdt:P856 ?sitelink ;
                          wdt:P1687 ?wikidataProperty.
                ?wikidataProperty wdt:P1630 ?formatterUrl
                FILTER (REGEX(str(?formatterUrl), ?domain) || REGEX(str(?sitelink), ?domain)).
            }
            union
            {
                BIND("{0}" AS ?domain).
                SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                ?subjects wdt:P856 ?sitelink ;
                FILTER REGEX(str(?sitelink), ?domain).
            }
        }
        '''.replace('\n',' ').replace('{0}', domain)
    query =  re.sub(' +',' ',query)
    return url_svc.sparql_get(query)
