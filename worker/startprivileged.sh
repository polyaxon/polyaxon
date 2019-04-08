chown -R polyaxon:polyaxon /polyaxon/logs/
cd /polyaxon/polyaxon
gosu privpolyaxon celery -A polyaxon $*
