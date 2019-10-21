# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import subprocess
import sys

import click

from polyaxon.deploy.operators.conda import CondaOperator
from polyaxon.exceptions import (
    PolyaxonClientException,
    PolyaxonConfigurationError,
    PolyaxonHTTPError,
    PolyaxonShouldExitError,
)
from polyaxon.tracking.utils.hashing import hash_value
from polyaxon.utils.formatting import Printer


def _get_conda_env_name(conda_env):
    conda_env_contents = open(conda_env).read() if conda_env else ""
    conda_tag = hash_value(conda_env_contents)
    return "polyaxon-{}".format(conda_tag)


def _run(
    ctx, name, owner, project_name, description, tags, specification, log, conda_env
):
    conda = CondaOperator()
    # cmd = CmdOperator()
    if not conda.check():
        raise PolyaxonConfigurationError("Conda is required to run this command.")

    envs = conda.execute(["env", "list", "--json"], is_json=True)
    env_names = [os.path.basename(env) for env in envs["envs"]]
    project_env_name = _get_conda_env_name(conda_env)
    if project_env_name not in env_names:
        click.echo("Creating conda environment {}".format(project_env_name))
        conda.execute(
            ["env", "create", "-n", project_env_name, "--file", conda_env], stream=True
        )

    cmd_bash, cmd_args = specification.run.get_container_cmd()
    cmd_args = ["source activate {}".format(project_env_name)] + cmd_args
    subprocess.Popen(cmd_bash + [" && ".join(cmd_args)], close_fds=True)


def run(
    ctx, name, owner, project_name, description, tags, specification, log, conda_env
):
    try:
        _run(
            ctx,
            name,
            owner,
            project_name,
            description,
            tags,
            specification,
            log,
            conda_env,
        )
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error("Could start local run.")
        Printer.print_error("Error message `{}`.".format(e))
        sys.exit(1)
    except Exception as e:
        Printer.print_error("Could start local run.")
        Printer.print_error("Unexpected Error: `{}`.".format(e))
        sys.exit(1)
