import psycopg2
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--username',
        type=str
    )
    parser.add_argument(
        '--password',
        type=str
    )
    parser.add_argument(
        '--host',
        type=str
    )
    parser.add_argument(
        '--db',
        type=str
    )
    parser.add_argument(
        '--port',
        type=str
    )
    args = parser.parse_args()
    arguments = args.__dict__

    username = arguments.pop('username')
    password = arguments.pop('password')
    host = arguments.pop('host')
    db = arguments.pop('db')
    port = arguments.pop('port')
    conn = psycopg2.connect(database=db, user=username, password=password, host=host, port=port)
    cur = conn.cursor()

    check_query = "select * from information_schema.tables where table_name='{}'".format('auth_user')
    cur.execute(check_query)
    if bool(cur.fetchall()):
        alter_query = "ALTER TABLE auth_user RENAME TO db_user"
        cur.execute(alter_query)
        conn.commit()
    conn.close()
