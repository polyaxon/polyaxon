from db.models.projects import Project

projects = Project.objects.select_related('user')

projects_details = projects.select_related('repo')
