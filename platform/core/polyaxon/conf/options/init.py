import conf

from options.registry import init

conf.subscribe(init.InitDockerImage)
conf.subscribe(init.InitImagePullPolicy)
