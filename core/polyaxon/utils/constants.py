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

NEWLINES = ("\n", "\r", "\r\n")

INIT_COMMAND = (
    "`polyaxon init -p PROJECT_NAME [--polyaxonfile] [--git-connection] [--git-url]`"
)

DEFAULT_IGNORE_LIST = """
.git
.eggs
eggs
lib
lib64
parts
sdist
var
*.pyc
*.swp
.DS_Store
./.polyaxon
"""

INIT_FILE_PATH = "polyaxonfile.yaml"

INIT_FILE_TEMPLATE = """---
version: 1.1
kind: component
run:
  kind: job
  container:
    # image: # image to use
    # command: # Command to use
"""

INIT_FILE = "init"
DEBUG_FILE = "debug"
