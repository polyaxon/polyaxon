import conf

from options.registry import mount_paths

conf.subscribe(mount_paths.MountPathsNvidia)
conf.subscribe(mount_paths.DirsNvidia)
