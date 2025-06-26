def schedule_jobs(scheduler):

    # schedule job functions
    def run_daily_task():
        print("✅ Running daily task at 12:01 AM")

    def run_hourly():
        print("⏰ Running every hour")

    def run_every_two():
        print("🔁 Running every 2 minutes")

    # add jobs to the scheduler with cron triggers
    scheduler.add_job(
        run_daily_task, 'cron', hour=0, minute=1, id='daily_task', replace_existing=True
    )
    scheduler.add_job(
        run_hourly, 'cron', minute=0, id='hourly_task', replace_existing=True
    )
    scheduler.add_job(
        run_every_two, 'cron', minute='*/2', id='every_two_minutes', replace_existing=True
    )
