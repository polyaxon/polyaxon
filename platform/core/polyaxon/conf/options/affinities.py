import conf

from options.registry import affinities

conf.subscribe(affinities.AffinitiesBuildJobs)
conf.subscribe(affinities.AffinitiesJobs)
conf.subscribe(affinities.AffinitiesExperiments)
conf.subscribe(affinities.AffinitiesNotebooks)
conf.subscribe(affinities.AffinitiesTensorboards)
