if [[ -z "${POLYAXON_SECURITY_CONTEXT_USER}" ]] || [[ -z "${POLYAXON_SECURITY_CONTEXT_GROUP}" ]]; then
    python3 polyaxon/manage.py $*
else
    ./create_user.sh
    chown -R polyaxon:polyaxon /polyaxon/logs/
    gosu polyaxon python3 polyaxon/manage.py $*
fi
