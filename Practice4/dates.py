#1Write a Python program to subtract five days from current date.
from datetime import datetime, timedelta
print(datetime.now() - timedelta(days=5))


#2 Write a Python program to print yesterday, today, tomorrow.
from datetime import datetime, timedelta

today = datetime.now()
print(today - timedelta(days=1))
print(today)
print(today + timedelta(days=1))



#3 Write a Python program to drop microseconds from datetime.
from datetime import datetime
print(datetime.now().replace(microsecond=0))


#4 Write a Python program to calculate two date difference in seconds.
from datetime import datetime

d1 = datetime(2026, 2, 20)
d2 = datetime(2026, 2, 25)

print((d2 - d1).total_seconds())