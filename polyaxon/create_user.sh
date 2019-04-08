#!/bin/bash

if [[ -z "${POLYAXON_SECURITY_CONTEXT_USER}" ]] || [[ -z "${POLYAXON_SECURITY_CONTEXT_GROUP}" ]]; then
    echo "Use default user"
else
    # add our user and group first to make sure their IDs get assigned consistently
    RUN groupadd -g ${POLYAXON_SECURITY_CONTEXT_USER} -r polyaxon && useradd -r -m -g polyaxon -G 0 -u ${POLYAXON_SECURITY_CONTEXT_GROUP} polyaxon
fi
