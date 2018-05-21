mkdir /polyaxon/logs
nginx -c /etc/nginx/nginx.conf -t
service nginx status
service nginx restart
service nginx status
uwsgi --ini web/uwsgi.nginx.ini
service nginx stop
service nginx status
