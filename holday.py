from datetime import datetime

holidays_exception = [
    '20220126',
    '20220127',
    '20220128',
    '20220228',
    '20220404',
    '20220405',
    '20220502',
    '20220603',
    '20220909',
    '20221010'
]

workdays_exception = [
]


def is_workday(day=None):
    today = datetime.today()
    day = day or today

    week_day = datetime.weekday(day) + 1
    is_work_day_in_week = week_day in range(1, 6)
    y, m, d = day.year, day.month, day.day
    day_str = f'{str(y).zfill(4)}{str(m).zfill(2)}{str(d).zfill(2)}'

    if day_str in workdays_exception:
        return True
    elif day_str in holidays_exception:
        return False
    elif is_work_day_in_week:
        return True
    else:
        return False


def is_holiday(day=None):
    today = datetime.today()
    day = day or today
    if is_workday(day):
        return False
    else:
        return True
