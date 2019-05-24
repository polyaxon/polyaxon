import conf

from options.registry import scheduler

conf.subscribe(scheduler.SchedulerCountdown)
conf.subscribe(scheduler.SchedulerCountdownDelayed)
