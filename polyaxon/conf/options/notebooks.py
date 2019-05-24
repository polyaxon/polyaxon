import conf

from options.registry import notebooks

conf.subscribe(notebooks.NotebooksDockerImage)
conf.subscribe(notebooks.NotebooksBackend)
conf.subscribe(notebooks.NotebooksPortRange)
conf.subscribe(notebooks.NotebooksMountCode)
