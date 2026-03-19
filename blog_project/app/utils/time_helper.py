from datetime import datetime

def time_ago(time):

    now = datetime.utcnow()
    diff = now - time

    seconds = diff.total_seconds()

    if seconds < 60:
        return "just now"

    minutes = seconds / 60
    if minutes < 60:
        return f"{int(minutes)} m"

    hours = minutes / 60
    if hours < 24:
        return f"{int(hours)} h"

    days = hours / 24
    if days < 7:
        return f"{int(days)} d"

    weeks = days / 7
    if weeks < 4:
        return f"{int(weeks)} w"

    months = days / 30
    if months < 12:
        return f"{int(months)} month"

    years = days / 365
    return f"{int(years)} year"