
from datetime import date

def get_school_week(today=None):
    if today is None:
        today = date.today()

    quarters = [
        (date(2024, 9, 1), date(2024, 10, 25)),  # I четверть
        (date(2024, 11, 4), date(2024, 12, 27)), # II четверть
        (date(2025, 1, 9), date(2025, 3, 21)),   # III четверть
        (date(2025, 4, 1), date(2025, 5, 25)),   # IV четверть
    ]

    start = date(2024, 9, 1)
    week_number = 1
    for q_start, q_end in quarters:
        if q_start <= today <= q_end:
            delta = (today - q_start).days
            week_number += delta // 7
            return week_number
        else:
            week_number += (q_end - q_start).days // 7 + 1
    return None
