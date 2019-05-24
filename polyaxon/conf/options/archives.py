import conf

from options.registry import archives

conf.subscribe(archives.ArchivesRootRepos)
conf.subscribe(archives.ArchivesRootArtifacts)
conf.subscribe(archives.ArchivesRootLogs)
