from db.models.projects import Project

projects = Project.objects.select_related('user', 'owner')

projects_details = projects.select_related('repo')
