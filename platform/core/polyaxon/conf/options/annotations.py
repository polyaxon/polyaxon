import conf

from options.registry import annotations

conf.subscribe(annotations.AnnotationsBuildJobs)
conf.subscribe(annotations.AnnotationsJobs)
conf.subscribe(annotations.AnnotationsExperiments)
conf.subscribe(annotations.AnnotationsNotebooks)
conf.subscribe(annotations.AnnotationsTensorboards)
