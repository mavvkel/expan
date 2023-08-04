import sys
from dispenser import Dispenser

if len(sys.argv) < 2:
    arg = 'Lista_transakcji_nr_0166335119_040823.csv'
else:
    arg = str(sys.argv[1])

dispenser = Dispenser(arg)

