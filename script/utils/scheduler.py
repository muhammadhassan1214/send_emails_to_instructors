from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from threading import Timer


def schedule_morning_and_night(task_func):
    """
    Schedules the task for the NEXT occurrence of either
    Morning (9 AM) or Night (9 PM) in America/New_York.
    """
    # --- CONFIGURATION ---
    # Change these values to set your specific times
    MORNING_HOUR = 9  # 9 AM
    NIGHT_HOUR = 21  # 9 PM (24-hour clock)
    TIMEZONE_STR = "America/New_York"
    # ---------------------

    # 1. Get current time in Ohio/NY
    ohio_tz = ZoneInfo(TIMEZONE_STR)
    now = datetime.now(ohio_tz)

    # 2. Define targets for "Today"
    morning_target = now.replace(hour=MORNING_HOUR, minute=0, second=0, microsecond=0)
    night_target = now.replace(hour=NIGHT_HOUR, minute=0, second=0, microsecond=0)

    # 3. Logic: If a target has passed for 'today', move it to 'tomorrow'
    if morning_target <= now:
        morning_target += timedelta(days=1)

    if night_target <= now:
        night_target += timedelta(days=1)

    # 4. Pick the earliest of the two valid future targets
    # Since we moved past targets to tomorrow, both dates are now in the future.
    # We just want the one happening soonest.
    next_run_time = min(morning_target, night_target)

    # 5. Calculate delay
    delay = (next_run_time - now).total_seconds()

    print(f"Current time (Ohio): {now.strftime('%Y-%m-%d %I:%M %p')}")
    print(f"Next run scheduled:  {next_run_time.strftime('%Y-%m-%d %I:%M %p')}")
    print(f"Waiting for:         {delay:.2f} seconds")

    # 6. Schedule the task
    t = Timer(delay, task_func)
    t.start()
    return t
