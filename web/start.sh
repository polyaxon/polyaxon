python3 -c "from polyaxon_nginx.generate import generate_nginx_conf; generate_nginx_conf('/polyaxon/web')"
rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-available/default
mkdir /etc/nginx/polyaxon
if [[ -z "${POLYAXON_SECURITY_CONTEXT_USER}" ]] || [[ -z "${POLYAXON_SECURITY_CONTEXT_GROUP}" ]]; then
    echo "Use default user"
else
    ../polyaxon/create_user.sh
    chown -R polyaxon:polyaxon /tmp/
    chown -R polyaxon:polyaxon /polyaxon/logs
    chown -R polyaxon:polyaxon /polyaxon/web
fi
cp web/uwsgi_params /etc/nginx/uwsgi_params
cp web/nginx.conf /etc/nginx/sites-available/polyaxon.config
mv web/polyaxon.base.conf /etc/nginx/polyaxon/polyaxon.base.conf
mv web/polyaxon.redirect.conf /etc/nginx/polyaxon/polyaxon.redirect.conf
ln -s /etc/nginx/sites-available/polyaxon.config /etc/nginx/sites-enabled/polyaxon.conf
mkdir -p /polyaxon/logs
nginx -c /etc/nginx/nginx.conf -t
service nginx status
service nginx restart
service nginx status
if [[ -z "${POLYAXON_SECURITY_CONTEXT_USER}" ]] || [[ -z "${POLYAXON_SECURITY_CONTEXT_GROUP}" ]]; then
    uwsgi --ini web/uwsgi.nginx.ini
else
    gosu polyaxon uwsgi --ini web/uwsgi.nginx.ini
fi
service nginx stop
service nginx status
