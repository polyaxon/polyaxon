POLYAXON_DOCKER_TEMPLATE = """
FROM {{ from_image }}

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
# Use bash as default shell, rather than sh
ENV SHELL /bin/bash

{% if nvidia_bin -%}
# Update with nvidia bin
ENV PATH="${PATH}:{{ nvidia_bin }}"
{% endif -%}

WORKDIR {{ workdir }}

{% if polyaxon_requirements_path -%}
COPY {{ polyaxon_requirements_path }} {{ workdir }}
{% endif -%}

{% if polyaxon_setup_path -%}
COPY {{ polyaxon_setup_path }} {{ workdir }}
{% endif -%}

{% if steps -%}
{% for step in steps -%}
RUN {{ step }}
{% endfor -%}
{% endif -%}

{% if env_vars -%}
{% for env_var in env_vars -%}
ENV {{env_var[0]}} {{env_var[1]}}
{% endfor -%}
{% endif -%}

COPY {{ folder_name }} {{ workdir }}
"""
