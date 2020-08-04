#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging
import time

from docker import APIClient
from docker.errors import APIError, BuildError
from urllib3.exceptions import ReadTimeoutError

from polyaxon.exceptions import PolyaxonBuildException
from polyaxon.schemas.types import V1UriType
from polyaxon.utils.log_levels import LogLevels

_logger = logging.getLogger("polyaxon.dockerizer")


class DockerMixin:
    IS_BUILD = None

    def _prepare_log_lines(self, log_line):  # pylint:disable=too-many-branches
        raw = log_line.decode("utf-8").strip()
        raw_lines = raw.split("\n")
        log_lines = []
        status = True
        for raw_line in raw_lines:
            try:
                json_line = json.loads(raw_line)

                if json_line.get("error"):
                    log_lines.append(
                        "{}: {}".format(
                            LogLevels.ERROR, str(json_line.get("error", json_line))
                        )
                    )
                    status = False
                else:
                    if json_line.get("stream"):
                        log_lines.append(
                            "Building: {}".format(json_line["stream"].strip())
                        )
                    elif json_line.get("status"):
                        if not self.is_pushing and not self.IS_BUILD:
                            self.is_pushing = True
                            log_lines.append("Pushing ...")
                    elif json_line.get("aux"):
                        log_lines.append(
                            "Pushing finished: {}".format(json_line.get("aux"))
                        )
                    else:
                        log_lines.append(str(json_line))
            except json.JSONDecodeError:
                log_lines.append("JSON decode error: {}".format(raw_line))
        return log_lines, status

    def _handle_logs(self, log_lines):
        for log_line in log_lines:
            print(log_line)  # pylint:disable=superfluous-parens

    def _handle_log_stream(self, stream):
        log_lines = []
        status = True
        try:
            for log_line in stream:
                new_log_lines, new_status = self._prepare_log_lines(log_line)
                log_lines += new_log_lines
                if not new_status:
                    status = new_status
                self._handle_logs(log_lines)
                log_lines = []
            if log_lines:
                self._handle_logs(log_lines)
        except (BuildError, APIError) as e:
            self._handle_logs(
                [
                    "{}: Could not build the image, encountered {}".format(
                        LogLevels.ERROR, e
                    )
                ]
            )
            return False

        return status


class DockerBuilder(DockerMixin):
    IS_BUILD = True

    def __init__(
        self, context, destination, credstore_env=None, registries=None, docker=None
    ):
        self.destination = destination

        self.context = context
        self._validate_registries(registries)
        self.registries = registries
        self.docker = docker or APIClient(version="auto", credstore_env=credstore_env)
        self.is_pushing = False

    @staticmethod
    def _validate_registries(registries):
        if not registries or isinstance(registries, V1UriType):
            return True

        for registry in registries:
            if not isinstance(registry, V1UriType):
                raise PolyaxonBuildException(
                    "A registry `{}` is not valid Urispec.".format(registry)
                )

        return True

    def check_image(self):
        return self.docker.images(self.destination)

    def login_private_registries(self):
        if not self.registries:
            return
        for registry in self.registries:
            self.docker.login(
                username=registry.user,
                password=registry.password,
                registry=registry.host,
                reauth=True,
            )

    def build(self, nocache=False, memory_limit=None):
        limits = {
            # Disable memory swap for building
            "memswap": -1
        }
        if memory_limit:
            limits["memory"] = memory_limit

        stream = self.docker.build(
            path=self.context,
            tag=self.destination,
            forcerm=True,
            rm=True,
            pull=True,
            nocache=nocache,
            container_limits=limits,
        )
        return self._handle_log_stream(stream=stream)


class DockerPusher(DockerMixin):
    IS_BUILD = False

    def __init__(self, destination, credstore_env=None, docker=None):
        self.destination = destination
        self.docker = docker or APIClient(version="auto", credstore_env=credstore_env)
        self.is_pushing = False

    def push(self):
        stream = self.docker.push(self.destination, stream=True)
        return self._handle_log_stream(stream=stream)


def _build(
    context, destination, nocache, docker=None, credstore_env=None, registries=None
):
    """Build necessary code for a job to run"""
    _logger.info("Starting build ...")

    # Build the image
    docker_builder = DockerBuilder(
        context=context,
        destination=destination,
        credstore_env=credstore_env,
        registries=registries,
        docker=docker,
    )
    docker_builder.login_private_registries()
    if docker_builder.check_image() and not nocache:
        # Image already built
        return docker_builder
    if not docker_builder.build(nocache=nocache):
        raise PolyaxonBuildException("The docker image could not be built.")
    return docker_builder


def build(
    context,
    destination,
    nocache,
    docker=None,
    credstore_env=None,
    registries=None,
    max_retries=3,
    sleep_interval=1,
):
    """Build necessary code for a job to run"""
    retry = 0
    is_done = False
    while retry < max_retries and not is_done:
        try:
            docker_builder = _build(
                context=context,
                destination=destination,
                docker=docker,
                nocache=nocache,
                credstore_env=credstore_env,
                registries=registries,
            )
            is_done = True
            return docker_builder
        except ReadTimeoutError:
            retry += 1
            time.sleep(sleep_interval)
    if not is_done:
        raise PolyaxonBuildException(
            "The docker image could not be built, client timed out."
        )


def push(destination, docker=None, max_retries=3, sleep_interval=1):
    docker_pusher = DockerPusher(destination=destination, docker=docker)
    retry = 0
    is_done = False
    while retry < max_retries and not is_done:
        try:
            if not docker_pusher.push():
                raise PolyaxonBuildException("The docker image could not be pushed.")
            else:
                is_done = True
        except ReadTimeoutError:
            retry += 1
            time.sleep(sleep_interval)

    if not is_done:
        raise PolyaxonBuildException(
            "The docker image could not be pushed, client timed out."
        )


def build_and_push(
    context,
    destination,
    nocache,
    credstore_env=None,
    registries=None,
    max_retries=3,
    sleep_interval=1,
):
    """Build necessary code for a job to run and push it."""
    # Build the image
    docker_builder = build(
        context=context,
        destination=destination,
        nocache=nocache,
        credstore_env=credstore_env,
        registries=registries,
        max_retries=max_retries,
        sleep_interval=sleep_interval,
    )
    push(
        destination=destination,
        docker=docker_builder.docker,
        max_retries=max_retries,
        sleep_interval=sleep_interval,
    )
