import re

m = re.search("Success! Got NOP_EXIT.", output)
if m:
    success = True
