import conf

from options.registry import sidecars

conf.subscribe(sidecars.SidecarsDockerImage)
conf.subscribe(sidecars.SidecarsImagePullPolicy)
conf.subscribe(sidecars.SidecarsSleepInterval)
