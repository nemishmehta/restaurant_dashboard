# Period

periods = {
    "Brunch": (0, 1200),
    "Lunch": (1200, 1500),
    "Tea": (1500, 1800),
    "dinner": (1800, 2359)
}


def get_period(time):
    time = time.split(":")
    time = int(time[0] + time[1])
    for period, (period_start, period_end) in periods.items():
        if period_start <= time <= period_end:
            return period


# To apply the function to the "order_time" column and create the "period" column
db["period"] = db["order_time"].apply(get_period)


# Seasons


"""
The first is necessary to convert the "order_time_creation" content in datetime objects. 
The whole process uses only Pandas methods (to_datetime and, later, date_range) so there is no need
to import the Datetime library. 
"""

db["order_creation_time"] = pd.to_datetime(db["order_creation_date"])


def season_of_date(date):
    year = str(date.year)
    # This dictionary must absolutely stay inside the function so the "year" is not out of scope
    seasons = {
        'spring': pd.date_range(start = year + '-03-21 00:00:00', end = year + '-06-20 00:00:00'),
        'summer': pd.date_range(start = year + '-06-21 00:00:00', end = year + '-09-22 00:00:00'),
        'autumn': pd.date_range(start = year + '-09-23 00:00:00', end = year + '-12-20 00:00:00')
    }
    if date in seasons['spring']:
        return 'spring'
    if date in seasons['summer']:
        return 'summer'
    if date in seasons['autumn']:
        return 'autumn'
    else:
        return 'winter'
