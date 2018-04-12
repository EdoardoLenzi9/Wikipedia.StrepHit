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

| File                      | Path                                      |
| --------------------------|:-----------------------------------------:|
| input dump                | ./assets/supervised_dataset.qs            |
| output dump               | ./assets/supervised_dataset_output.qs     |
| error log                 | ./assets/supervised_dataset_errors.log    |
| json with new mappings    | ./assets/supervised_dataset_errors.log    |

## TODO
    1. every url template pattern can have only one slot ($1) or more?  
    2. run async tasks in parallel (output dump rows order)
    3. optimize sparql query, take only best fit links
