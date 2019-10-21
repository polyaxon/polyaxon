#!/bin/bash
cd /polyaxon/polyaxon
if [[ -z "${POLYAXON_SECURITY_CONTEXT_USER}" ]] || [[ -z "${POLYAXON_SECURITY_CONTEXT_GROUP}" ]]; then
    python3 -m sanic streams.api.app $*
else
    ./create_user.sh
    gosu polyaxon python3 -m sanic streams.api.app $*
fi
