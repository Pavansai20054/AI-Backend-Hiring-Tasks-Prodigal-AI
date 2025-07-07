from datetime import datetime, timedelta

def simulate_days(run_once_fn, n_days):
    now = datetime.now()
    for i in range(n_days):
        day = now + timedelta(days=i)
        run_once_fn(day_str=day.strftime("%Y-%m-%d"))