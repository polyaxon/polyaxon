import conf

from options.registry import deployments

conf.subscribe(deployments.PlatformEnvironmentVersion)
conf.subscribe(deployments.ChartVersion)
conf.subscribe(deployments.ChartIsUpgrade)
conf.subscribe(deployments.CliMinVersion)
conf.subscribe(deployments.CliLatestVersion)
conf.subscribe(deployments.PlatformMinVersion)
conf.subscribe(deployments.PlatformLatestVersion)
conf.subscribe(deployments.LibMinVersion)
conf.subscribe(deployments.LibLatestVersion)
