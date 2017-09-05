

import re

date = "Sep. 14, 2017, noon PT"

result = re.match(r'[^\s]+\. [0-9]+, [0-9]+',date)
print result.group(0)






