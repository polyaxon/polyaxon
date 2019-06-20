if [[ -z "${POLYAXON_SECURITY_CONTEXT_USER}" ]] || [[ -z "${POLYAXON_SECURITY_CONTEXT_GROUP}" ]]; then
    python3 polyaxon/manage.py $*
else
    ./polyaxon/create_user.sh
    gosu polyaxon python3 polyaxon/manage.py $*
fi
