# Wikipedia.StrepHit

simple script in python 2.7 that adds references to a wikidata .qs dump 

## StartUp
```sh
    sh compile.sh
```

or

```sh
    python main.py
```

## Assets

| File                          | Path                                              |
| ------------------------------|:-------------------------------------------------:|
| input dump                    | ./assets/supervised_dataset.qs                    |
| output dump                   | ./assets/supervised_dataset_output.qs             |
| error log                     | ./assets/supervised_dataset_errors.log            |
| json with mappings            | ./assets/supervised_dataset_mappings.json         |
| json with unknown mappings    | ./assets/supervised_dataset_unknown_mappings.json |

## domain/localizations.py
Here you can manage all constants, strings, paths and urls of the script.

**ie** 
```python
    MAP_ALL_RESPONSES = False   # this mode increase the memory usage but also the speed of the script (if 
                                # your mappings aren't complete)
    IS_ASYNC_MODE = False       # this mode compute on a new thread every row of the dataset 
                                # (this increase the speed of the script but the output rows order can change)
```
## TODO
    1. async_mode and map_all_responses_mode need more testing and fixes
