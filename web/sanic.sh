chown -R polyaxon:polyaxon /polyaxon/logs/
cd /polyaxon/polyaxon
gosu polyaxon python3 -m sanic streams.api.app $*
