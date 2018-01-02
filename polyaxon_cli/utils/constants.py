# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

INIT_COMMAND = "`polyaxon init PROJECT_NAME [--run|--model]`"

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

INIT_FILE = 'polyaxonfile.yml'
INIT_FILE_PROJECT_SECTION = "# set you project name here. If you don't have project please create one first."

INIT_FILE_MODEL_TEMPLATE = """---
version: 1

project:
  name: {}

settings:
  logging:
    level: INFO

model:
  # set you model
"""

INIT_FILE_RUN_TEMPLATE = """---
version: 1

project:
  name: {}

run:
  # image: # Image name to use
  # cmd: # Command to use
"""

INIT_FILE_MODEL = 'model'
INIT_FILE_RUN = 'run'

INIT_FILE_TEMPLATES = {
    INIT_FILE_MODEL: INIT_FILE_MODEL_TEMPLATE,
    INIT_FILE_RUN: INIT_FILE_RUN_TEMPLATE
}
