#!C:\Code\Wikipedia.StrepHit\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'Wikipedia.StrepHit','console_scripts','main'
__requires__ = 'Wikipedia.StrepHit'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('Wikipedia.StrepHit', 'console_scripts', 'main')()
    )
