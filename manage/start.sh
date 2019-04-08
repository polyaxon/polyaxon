cd /polyaxon/polyaxon
if [[ -z "${POLYAXON_SECURITY_CONTEXT_USER}" ]] || [[ -z "${POLYAXON_SECURITY_CONTEXT_GROUP}" ]]; then
    python3 manage.py $*
else
    ./create_user.sh
    chown -R polyaxon:polyaxon /polyaxon/logs/
    gosu polyaxon python3 manage.py $*
fi
