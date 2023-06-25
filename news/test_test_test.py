import datetime
date = datetime.datetime.today()
week = str(int(date.strftime("%V"))-1)
print(date)
print(week, type(week))