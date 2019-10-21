import conf

from options.registry import stats

conf.subscribe(stats.StatsDefaultPrefix)
