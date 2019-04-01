python3 -c "from polyaxon_nginx.generate import generate_nginx_conf; generate_nginx_conf('/polyaxon/web')"
mv web/polyaxon.base.conf /etc/nginx/polyaxon/polyaxon.base.conf
mkdir /polyaxon/logs
nginx -c /etc/nginx/nginx.conf -t
service nginx status
service nginx restart
service nginx status
uwsgi --ini web/uwsgi.nginx.ini
service nginx stop
service nginx status
