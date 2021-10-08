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

POLYAXON_DOCKER_TEMPLATE = """
FROM {{ image }}

{% if lang_env -%}
ENV LC_ALL {{ lang_env }}
ENV LANG {{ lang_env }}
ENV LANGUAGE {{ lang_env }}
{% endif -%}

{% if shell %}
ENV SHELL {{ shell }}
{% endif -%}

{% if path -%}
{% for path_step in path -%}
ENV PATH="${PATH}:{{ path_step }}"
{% endfor -%}
{% endif -%}

{% if env -%}
{% for env_step in env -%}
ENV {{ env_step[0] }} {{ env_step[1] }}
{% endfor -%}
{% endif -%}

WORKDIR {{ workdir }}

{% if copy -%}
{% for copy_step in copy -%}
COPY {{ copy_step[0] }} {{ copy_step[1] }}
{% endfor -%}
{% endif -%}

{% if run -%}
{% for step in run -%}
RUN {{ step }}
{% endfor -%}
{% endif -%}

{% if post_run_copy -%}
{% for copy_step in post_run_copy -%}
COPY {{ copy_step[0] }} {{ copy_step[1] }}
{% endfor -%}
{% endif -%}

{% if uid and gid -%}
# Drop root user and use Polyaxon user
RUN groupadd -g {{ gid }} -r polyaxon && useradd -r -m -g polyaxon -u {{ uid }} {{ username }}
{% endif -%}

{% if workdir_path -%}
COPY {{ workdir_path }} {{ workdir }}
{% endif -%}
"""
