import click
import click_completion

from polyaxon_cli.logger import clean_outputs


@click.command()
@click.option('--append/--overwrite', help="Append the completion code to the file", default=None)
@click.argument('shell',
                required=False,
                type=click_completion.DocumentedChoice(click_completion.core.shells))
@click.argument('path', required=False)
@clean_outputs
def completion(append, shell, path):
    """Install the auto-completion for polyaxon-cli"""
    shell, path = click_completion.core.install(shell=shell, path=path, append=append)
    click.echo('%s completion installed in %s' % (shell, path))
