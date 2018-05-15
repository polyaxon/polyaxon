import os


def get_env_ssl_enabled():
    return os.getenv('POLYAXON_SSL_ENABLED', None)


def get_env_server_name():
    return os.getenv('POLYAXON_SERVER_NAME', None)


def generate_nginx_ssl_conf():
    # if not get_env_ssl_enabled():
    #     return

    server_name = get_env_server_name()
    if not server_name:
        print('SSL enabled but server name was not provided, default to default config.')

    with open('./nginx_ssl.conf') as f:
        result = f.read()
        result = result % (server_name, server_name)

    with open('./nginx.conf', 'w') as f:
        f.write(result)


generate_nginx_ssl_conf()
