import calendar

def get_weekday_count(year):
    total_weekdays = 0
    for month in range(1, 13):
        for day in range(1, calendar.monthrange(year, month)[1] + 1):
            if calendar.weekday(year, month, day) < 5:
                total_weekdays += 1
    return total_weekdays