import conf

from options.registry import downloads

conf.subscribe(downloads.DownloadRootArtifacts)
conf.subscribe(downloads.DownloadRootLogs)
