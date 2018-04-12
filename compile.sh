#! /bin/bash
clear
find . -type f -name '*.pyc' -delete
python main.py 
sh clean.sh