napis = "Queens,40.732731,-73.888603,844000.0"


import re

pattern = '\d+\.\d*,-\d+\.\d*'

prog = re.compile(pattern)
result = prog.match(napis)

print(result)