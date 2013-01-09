#!/usr/bin/python

import sys

from pyschedules.retrieve import get_qam_map

if len(sys.argv) < 2:
    print("Please provide a lineup-ID.")
    sys.exit()

lineup_id = sys.argv[1]

try:
    print(get_qam_map(lineup_id))
except Exception as e:
    print(str(e))

