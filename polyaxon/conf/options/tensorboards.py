import conf

from options.registry import tensorboards

conf.subscribe(tensorboards.TensorboardsDockerImage)
conf.subscribe(tensorboards.TensorboardsPortRange)
