# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click
import sys

from marshmallow import ValidationError
from polyaxon_client.exceptions import PolyaxonShouldExitError
from polyaxon_schemas.project import ProjectConfig

from polyaxon_cli.logger import logger
from polyaxon_cli.managers.project import ProjectManager
from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_cli.utils.formatting import (
    Printer,
    get_meta_response,
    list_dicts_to_tabulate,
    dict_tabulate
)


def get_project_local(project):
    project = project or ProjectManager.get_value('uuid').hex
    if not project:
        Printer.print_error('Please provide a valid project uuid, or init a new project.')
        sys.exit(0)

    return project


@click.group()
def project():
    """CRUD operations for projects."""
    pass


@project.command()
@click.option('--name', required=True, type=str,
              help='Name of the project, must be unique for the same user')
@click.option('--description', type=str, help='Description of the project,')
def create(name, description):
    """Create a new project.

    Example:

    ```
    polyaxon project create --name=cats-vs-dogs --description=Image Classification with Deep Learning
    ```
    """
    try:
        project_config = ProjectConfig.from_dict(dict(name=name, description=description))
    except ValidationError:
        Printer.print_error('Project name should contain only alpha numericals, "-", and "_".')
        sys.exit(0)

    try:
        project = PolyaxonClients().project.create_project(project_config)
        PolyaxonClients.handle_response(
            project, error_message='The project was not created, '
                                   'may be a project with same name already exists.')
    except PolyaxonShouldExitError as e:
        logger.exception(e)
        sys.exit(0)

    Printer.print_success("Project `{}` was created successfully with uuid `{}`.".format(
        project.name, project.uuid.hex))


@project.command()
@click.option('--page', type=int, help='To paginate through the list of projects.')
def list(page):
    """List projects."""
    page = page or 1
    try:
        response = PolyaxonClients().project.list_projects(page=page)
        PolyaxonClients.handle_response(
            project, error_message='The project was not created, '
                                   'may be a project with same name already exists.')
    except PolyaxonShouldExitError as e:
        logger.exception(e)
        sys.exit(0)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Projects for current user')
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No projects found for current user')

    objects = list_dicts_to_tabulate([o.to_dict() for o in response['results']])
    if objects:
        Printer.print_header("Projects:")
        dict_tabulate(objects, is_list_dict=True)


@project.command()
@click.argument('project', type=str, required=False)
def get(project):
    """Get project by uuid, default to the current project.

    Examples:

         To get current project:
    ```
    polyaxon project get
    ```

        To get a project by uuid
    ```
    polyaxon project get 50c62372137940ca8c456d8596946dd7
    ```
    """
    project = get_project_local(project)

    try:
        response = PolyaxonClients().project.get_project(project)
        PolyaxonClients.handle_response(
            response, error_message='no project was found with `{}`'.format(project))
    except PolyaxonShouldExitError as e:
        logger.exception(e)
        sys.exit(0)

    response = response.to_dict()
    Printer.print_header("Project info:")
    dict_tabulate(response)


@project.command()
@click.argument('project', type=str)
def delete(project):
    """Delete project."""
    project = get_project_local(project)

    if not click.confirm("Are sure you want to delete project `{}`".format(project)):
        click.echo('Existing without deleting project.')
        sys.exit(0)

    try:
        response = PolyaxonClients().project.delete_project(project)
        PolyaxonClients.handle_response(
            project, error_message='The project was not deleted.')
    except PolyaxonShouldExitError as e:
        logger.exception(e)
        sys.exit(0)

    if response.status_code == 204:
        Printer.print_success("Project `{}` was delete successfully".format(project))


@project.command()
@click.argument('project', type=str, required=False)
@click.option('--name', type=str,
              help='Name of the project, must be unique for the same user,')
@click.option('--description', type=str, help='Description of the project,')
def update(project, name, description):
    """Update project.

    Example:

    ```
    polyaxon update 50c62372137940ca8c456d8596946dd7 --description=Image Classification with Deep Learning using TensorFlow
    ```
    """
    project = get_project_local(project)

    update_dict = {}
    if name:
        update_dict['name'] = name

    if description:
        update_dict['description'] = description

    if not update_dict:
        Printer.print_warning('No argument was provided to update the project.')
        sys.exit(0)

    try:
        response = PolyaxonClients().project.update_project(project, update_dict)
        PolyaxonClients.handle_response(
            project, error_message='The project was not updated.')
    except PolyaxonShouldExitError as e:
        logger.exception(e)
        sys.exit(0)

    Printer.print_success("Project updated.")
    response = response.to_dict()
    Printer.print_header("Project info:")
    dict_tabulate(response)


@project.command()
@click.argument('project', type=str, required=True)
@click.option('--page', type=int, help='To paginate through the list of projects.')
def experiment_groups(project, page):
    """List experiment groups for this project"""
    project = get_project_local(project)

    page = page or 1
    try:
        response = PolyaxonClients().project.list_experiment_groups(project, page=page)
    except PolyaxonShouldExitError as e:
        logger.exception(e)
        sys.exit(0)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Experiment groups for project `{}`.'.format(project))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No experiment groups found for project `{}`.'.format(project))

    objects = list_dicts_to_tabulate([o.to_dict() for o in response['results']])
    if objects:
        Printer.print_header("Experiment groups:")
        objects.pop('project')
        dict_tabulate(objects, is_list_dict=True)


@project.command()
@click.argument('project', type=str, required=True)
@click.option('--page', type=int, help='To paginate through the list of projects.')
def experiments(project, page):
    """List experiments for this project"""
    project = get_project_local(project)

    page = page or 1
    try:
        response = PolyaxonClients().project.list_experiments(project, page=page)
    except PolyaxonShouldExitError as e:
        logger.exception(e)
        sys.exit(0)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Experiments for project `{}`.'.format(project))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No experiments found for project `{}`.'.format(project))

    objects = list_dicts_to_tabulate([o.to_dict() for o in response['results']])
    if objects:
        Printer.print_header("Experiments:")
        objects.pop('project')
        dict_tabulate(objects, is_list_dict=True)
