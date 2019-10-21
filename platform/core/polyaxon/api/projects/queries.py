from db.models.projects import Project

projects = Project.objects.prefetch_related('user', 'owner')

projects_details = projects.select_related('repo')
