
from datetime import datetime

def get_time_elapsed(afk_date):
    elapsed_time = datetime.utcnow() - afk_date
    seconds = elapsed_time.total_seconds()
    days = seconds // 86400
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    string = ""
    if days != 0.0:
        string += f"{round(days)} day" if days == 1.0 else f"{round(days)} days"

    elif hours != 0.0:
        string += f"{round(hours)} hour" if hours == 1.0 else f"{round(hours)} hours"

    elif minutes != 0.0:
        string += f"{round(minutes)} minute" if minutes == 1.0 else f"{round(minutes)} minutes"
    
    else:
        string += f"{round(seconds)} second" if hours == 1.0 else f"{round(seconds)} seconds"
    return string
