# Polyaxon
from polyaxon.client import ProjectClient
from polyaxon_sdk.rest import ApiException


def check_project(name: str):
    project = ProjectClient(project=name)
    try:
        project.refresh_data()
    except ApiException:
        project.project_data.name = 'sgd-classifier'
        project.create(project.project_data)
