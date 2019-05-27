# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

POLYAXON_DOCKER_TEMPLATE = """
FROM {{ from_image }}

{% if lang_env -%}
ENV LC_ALL {{ lang_env }}
ENV LANG {{ lang_env }}
ENV LANGUAGE {{ lang_env }}
{% endif -%}
# Use bash as default shell, rather than sh
ENV SHELL /bin/bash

{% if uid and gid -%}
# Drop root user and use Polyaxon user
RUN groupadd -g 2222 -r polyaxon && useradd -r -m -g polyaxon -u 2222 polyaxon
{% endif -%}

{% if nvidia_bin -%}
# Update with nvidia bin
ENV PATH="${PATH}:{{ nvidia_bin }}"
{% endif -%}

{% if env_vars -%}
{% for env_var in env_vars -%}
ENV {{env_var[0]}} {{env_var[1]}}
{% endfor -%}
{% endif -%}

WORKDIR {{ workdir }}

{% if polyaxon_requirements_path -%}
COPY {{ polyaxon_requirements_path }} {{ workdir }}
{% endif -%}

{% if polyaxon_conda_env_path -%}
COPY {{ polyaxon_conda_env_path }} {{ workdir }}
{% endif -%}

{% if polyaxon_setup_path -%}
COPY {{ polyaxon_setup_path }} {{ workdir }}
{% endif -%}

{% if build_steps -%}
{% for step in build_steps -%}
RUN {{ step }}
{% endfor -%}
{% endif -%}

{% if copy_code -%}
COPY {{ folder_name }} {{ workdir }}
{% endif -%}
"""

POLYAXON_DOCKERFILE_NAME = 'Dockerfile'
