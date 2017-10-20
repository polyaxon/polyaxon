import pip
import pkg_resources
import click

from polyaxon_schemas.polyaxonfile.logger import logger


PROJECT_CLI_NAME = "polyaxon-cli"
PROJECT_NAME = "polyaxon"


def pip_upgrade(project_name=PROJECT_CLI_NAME):
    pip.main(["install", "--upgrade", project_name])


def get_version(pkg):
    try:
        version = pkg_resources.get_distribution(pkg).version
        return version
    except pkg_resources.DistributionNotFound:
        logger.error('`{}` is not installed'.format(pkg))


@click.command()
@click.option('--all', '-a', is_flag=True, default=False,
              help='Version of the project, if True the version of the cli '
                   'otherwise the version the polyaxon library.')
def version(all):
    """Prints the current version of the CLI."""
    project_name = PROJECT_NAME if all else PROJECT_CLI_NAME
    version = get_version(project_name)
    logger.info(version)


@click.command()
@click.option('--all', '-a', is_flag=True, default=False,
              help='Upgrade the project, if True upgrade the cli '
                   'otherwise upgrade the polyaxon library.')
def upgrade(all):
    """Install/Upgrade polyaxon or polyxon-cli."""
    try:
        project_name = PROJECT_NAME if all else PROJECT_CLI_NAME
        pip_upgrade(project_name)
    except Exception as e:
        logger.error(e)
