import conf

from options.registry import access

conf.subscribe(access.AccessGit)
conf.subscribe(access.AccessRegistry)
