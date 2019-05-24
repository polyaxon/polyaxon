import conf

from options.registry import ttl

conf.subscribe(ttl.TTLWatchStatuses)
conf.subscribe(ttl.TTLEphemeralToken)
conf.subscribe(ttl.TTLToken)
conf.subscribe(ttl.TTLHeartbeat)
