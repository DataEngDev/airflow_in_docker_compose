# python 3 
import yaml
import os
import psycopg2

with open('.creds.yml') as f:
    config = yaml.load(f)


LOCAL_SSH_USER = config['ssh_local']['user']
LOCAL_SSH_USER_PASSWORD = config['ssh_local']['password']


def insert_local_ssh_conn(cursor):
    sql = """
        INSERT INTO public."connection"
        (conn_id, conn_type, host, "schema", login, password, port, extra, is_encrypted, is_extra_encrypted)
        VALUES('local_ssh_default', 'ssh', '192.168.0.178', '', '{DEFAULT_SLACK_API_TOKEN}', '{DEFAULT_SLACK_API_TOKEN}', 22, '', false, false);
        """.format(
            DEFAULT_SLACK_API_TOKEN=SLACK_API_TOKEN,
            DEFAULT_SLACK_API_TOKEN2=SLACK_API_TOKEN
            )
    cursor.execute(sql)


def main():
    # config 
    conn_string = "host='airflow' dbname='airflow' user='airflow' password='airflow'"
    conn = psycopg2.connect(conn_string)
    conn.autocommit = True
    try: 
        cursor = conn.cursor()
        print('Inserting local ssh conn')
        insert_local_ssh_conn(cursor)

    except Exception as e:
        print ('Insert credentials failed.. ')
        print (e)

if __name__ == '__main__':
	main()
