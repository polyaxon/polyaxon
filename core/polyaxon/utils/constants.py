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

NEWLINES = ("\n", "\r", "\r\n")

INIT_COMMAND = "`polyaxon init PROJECT_NAME [--polyaxonfile]`"

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
DEBUG_FILE_PATH = "polyaxonfile.debug.yaml"

INIT_FILE_TEMPLATE = """---
version: 1

kind: job

container:
  # image: # image to use
  # command: # Command to use
"""

DEBUG_FILE_TEMPLATE = """---
container:
  # command: sleep 120 
"""

INIT_FILE = "init"
DEBUG_FILE = "debug"

PLX_FILE_TEMPLATES = {INIT_FILE: INIT_FILE_TEMPLATE, DEBUG_FILE: DEBUG_FILE_TEMPLATE}
