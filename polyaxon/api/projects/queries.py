from django.db.models import Count, Q

from db.models.projects import Project

projects = Project.objects.select_related('user')
projects_details = projects.select_related('repo').annotate(
    Count('experiments', distinct=True),
    Count('jobs', distinct=True),
    Count('build_jobs', distinct=True),
    Count('experiment_groups', distinct=True)).annotate(
    independent_experiments__count=Count(
        'experiments',
        filter=Q(experiments__experiment_group__isnull=True),
        distinct=True))
