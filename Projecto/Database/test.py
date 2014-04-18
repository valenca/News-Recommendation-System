from datetime import datetime
from re import compile as rcompile

date1 = 'Thu, 17 Apr 14 14:12:35 +0100'
date2 = 'Thu, 17 Apr 2014 20:38:02 GMT'

date = datetime.strptime(date1, rcompile('%a|%A, %d %b|%B|%m %y|%Y %H:%M:%S %z|%Z'))
print date
