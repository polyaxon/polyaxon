chown -R polyaxon:polyaxon /polyaxon/logs/
cd /polyaxon/polyaxon
gosu polyaxon celery -A polyaxon $*
