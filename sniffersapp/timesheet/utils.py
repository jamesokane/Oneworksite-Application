import datetime

def days_hours_minutes(td):
    return td.days, td.seconds // 3600, (td.seconds // 60) % 60

def calculate_hours(docket, lunch=True, smoko=True ):
    if not docket.start_time or not docket.finish_time:
        return 0, 0
    combine = datetime.datetime.combine
    shift_length = combine(docket.timesheet_date, docket.finish_time) - combine(docket.timesheet_date, docket.start_time)
    if lunch:
        shift_length = shift_length - datetime.timedelta(minutes=int(docket.lunch))
        if smoko:
            shift_length = shift_length - datetime.timedelta(minutes=int(docket.smoko))
    days, hours, mins = days_hours_minutes(shift_length)
    return (hours, mins)
