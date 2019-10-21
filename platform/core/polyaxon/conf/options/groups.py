import conf

from options.registry import groups

conf.subscribe(groups.GroupsCheckInterval)
conf.subscribe(groups.GroupsChunks)
