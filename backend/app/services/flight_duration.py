from datetime import datetime, time


def calculate_duration_minutes(start_time: time, end_time: time | None) -> int:
    if end_time is None:
        return 0
    start = datetime.combine(datetime.min.date(), start_time)
    end = datetime.combine(datetime.min.date(), end_time)
    return max(0, int((end - start).total_seconds() // 60))
