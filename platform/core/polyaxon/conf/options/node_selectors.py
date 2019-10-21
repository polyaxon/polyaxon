import conf

from options.registry import node_selectors

conf.subscribe(node_selectors.NodeSelectorsBuildJobs)
conf.subscribe(node_selectors.NodeSelectorsJobs)
conf.subscribe(node_selectors.NodeSelectorsExperiments)
conf.subscribe(node_selectors.NodeSelectorsNotebooks)
conf.subscribe(node_selectors.NodeSelectorsTensorboards)
