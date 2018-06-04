import click
import main

@click.group(help='''
Simple script in python 2.7 that adds references to a wikidata .qs dump.\n

Assets: \n
    (Default) INPUT FILE: \t assets\supervised_dataset.qs\n
    (Default) OUTPUT FILE: \t supervised_dataset_output.qs\n
    (Default) REFRESHED URLS LOG: \t supervised_dataset_refreshed_urls.json\n
    (Default) ERRORS LOG FILE: \t supervised_dataset_errors.log\n
    (Default) SOURCE MAPPINGS FILE: \t supervised_dataset_source_mappings.json\n
    (Default) AUTOGENERATED MAPPINGS FILE: \t supervised_dataset_mappings.json\n
    (Default) AUTOGENERATED UNKNOWN MAPPINGS FILE: \t supervised_dataset_unknown_mappings.json\n

Manage your configs in "domain/localizations.py":\n
    * (bool) LOAD_MAPPINGS: loads autogenerated mappings from "assets/supervised_dataset_mappings.json" and "assets/supervised_dataset_unknown_mappings.json" files. \n
    * (bool) MAP_ALL_RESPONSES: when you call add_references procedure, in case of an unmapped 'reference URL' (P854) inserts in "supervised_dataset_mappings.json" every record of the result sparql-query (business/queries/sitelink_queries.py). \n
    * (bool) IS_ASYNC_MODE: when you call add_references procedure, processes each row on a new thread. \n
    * (bool) DELETE_ROW: when you call refresh procedure, deletes rows with unrechable 'reference URL' (P854). \n
    * (bool) REFRESH_UNKNOWN_DOMAINS: when you call refresh procedure, replaces old urls with updated urls in case of site redirection. \n
    * [Here you can also customize every default path of your assets]

Notes:
    * Async mode and MAP_ALL_RESPONSES mode need more testing
''')
def cli():
    pass

@click.command(help="Refresh URLs of your .qs input dump, for each row check if 'reference URL' (P854) is reachable and, in case of redirect, updates it")
def refresh():
    main.refresh() 

@click.command(help="For each row of your .qs input dump analyzes 'reference URL' (P854) property and generate a 'stated in' (P248) propery (where possible)")
def add_references():
    main.add_references() 

@click.command(help="Calls sequentially refresh and add_references commands") 
def refresh_and_add():
    main.refresh_and_add() 

@click.command(help="For each row of your .qs input dump checks if 'reference URL' (P854) is just mapped in your mapping files (and logs if not)")
def export_unmapped():
    main.export_unmapped()

cli.add_command(refresh)  
cli.add_command(add_references)
cli.add_command(refresh_and_add)
cli.add_command(export_unmapped)