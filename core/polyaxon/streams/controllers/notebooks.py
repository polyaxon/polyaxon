#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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

import os

import nbformat

from nbconvert import HTMLExporter


def render_notebook(archived_path: str, check_cache=True):
    html_path = archived_path.split(".ipynb")[0] + ".html"
    if os.path.exists(html_path):
        if check_cache:
            # file already exists
            return html_path
        else:
            os.remove(html_path)

    with open(os.path.abspath(archived_path)) as f:
        read_data = f.read()
        notebook = nbformat.reads(read_data, as_version=4)
        html_exporter = HTMLExporter()
        html_exporter.template_file = "basic"
        (body, resources) = html_exporter.from_notebook_node(notebook)
        html_file = "<style>" + resources["inlining"]["css"][0] + "</style>" + body
        with open(html_path, "w") as destination:
            destination.write(html_file)
        return html_path
