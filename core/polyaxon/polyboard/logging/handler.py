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

from collections import deque
from typing import Callable

from polyaxon.containers.names import MAIN_JOB_CONTAINER
from polyaxon.polyboard.logging.schemas import V1Log, V1Logs
from polyaxon.utils.formatting import Printer
from polyaxon.utils.tz_utils import local_datetime


def get_logs_handler(
    show_timestamp=True, all_containers=False, all_info=False
) -> Callable:
    colors = deque(Printer.COLORS)
    job_to_color = {}
    if all_info:
        all_containers = True

    def handle_log_line(log: V1Log):
        log_dict = log.to_dict()
        log_line = ""
        if log.timestamp and show_timestamp:
            date_value = local_datetime(log_dict.get("timestamp"))
            log_line = Printer.add_color(date_value, "white") + " | "

        def get_container_info():
            if container_info in job_to_color:
                color = job_to_color[container_info]
            else:
                color = colors[0]
                colors.rotate(-1)
                job_to_color[container_info] = color
            return Printer.add_color(container_info, color) + " | "

        if not all_containers and log.container != MAIN_JOB_CONTAINER:
            return log_line

        if all_info:
            container_info = ""
            if log.node:
                log_line += Printer.add_color(log_dict.get("node"), "white") + " | "
            if log.pod:
                log_line += Printer.add_color(log_dict.get("pod"), "white") + " | "
            if log.container:
                container_info = log_dict.get("container")

            log_line += get_container_info()

        log_line += log_dict.get("value")
        Printer.log(log_line, nl=True)

    def handle_log_lines(logs: V1Logs):
        for log in logs.logs:
            if log:
                handle_log_line(log=log)

    return handle_log_lines
