from django.db.models import Count

from db.models.build_jobs import BuildJob

builds = BuildJob.objects.select_related(
    'user',
    'project',
    'project__user',
    'status')

builds_details = builds.select_related('code_reference').annotate(
    Count('experiments', distinct=True),
    Count('jobs', distinct=True))
