from db.models.build_jobs import BuildJob

builds = BuildJob.objects.select_related('status')
builds = builds.prefetch_related(
    'user',
    'project',
    'project__user',)

builds_details = builds.select_related('code_reference')
