import conf

from options.registry import cleaning

conf.subscribe(cleaning.CleaningIntervalsActivityLogs)
conf.subscribe(cleaning.CleaningIntervalsNotifications)
conf.subscribe(cleaning.CleaningIntervalsArchives)
