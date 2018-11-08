from db.models.projects import Project

projects = Project.objects.select_related('user', 'owner_content_type')

projects_details = projects.select_related('repo')
