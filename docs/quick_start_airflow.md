### Quick Start

1. Launch airflow via docker-compose
```bash
git clone https://github.com/DataEngDev/airflow_in_docker_compose.git
cd airflow_in_docker_compose

### V1
docker-compose -f docker-compose-2.0-with-celery-executor.yml up --buil
# shut down the service
docker-compose -f docker-compose-2.0-with-celery-executor.yml down

### V2
docker-compose -f docker-compose-with-celery-executor.yml up --build
# account, password : admin, admin
```

2. Init connection, variables..
```bash
docker ps -a

# docker exec -it 27dd2bd742f9 /bin/sh -c "ls files"
docker exec -it 27dd2bd742f9 /bin/sh -c "cd files && python script/insert_conn.py"
docker exec -it 27dd2bd742f9 /bin/sh -c "cd files && python script/insert_variable.py"
```

3. Install py packages
```bash
docker ps -a 

#docker exec -it 56d9da22d7cf bash
docker exec -it <airflow_in_docker_compose_worker_1's id> bash

pip install --upgrade pip
pip install pywebhdfs
```

4. Update connection
```bash
# via psql
# step 1) login to postgre shell
psql --u airflow 

# step 2) select DB
\c airflow

# step 3) set up local ssh connection
INSERT INTO connection VALUES (456, 'hadoop@local', 'ssh', '192.168.0.178','','yennan.liu','<password>',22,'');

# step 4) double check
airflow=# 
airflow=# select * from connection;
 id  |   conn_id    | conn_type |     host      | schema |   login    |  password  | port | extra | is_encrypted | is_extra_encrypted 
-----+--------------+-----------+---------------+--------+------------+------------+------+-------+--------------+--------------------
 456 | hadoop@local | ssh       | 192.168.0.178 |        | yennan.liu | *** |   22 |       |              | 
(1 row)

# or check here 
# http://localhost:8080/admin/connection/
``` 

```python
# via python
import yaml
import os
import psycopg2

LOCAL_SSH_USER = <LOCAL_SSH_USER>
LOCAL_SSH_USER_PASSWORD = <LOCAL_SSH_USER_PASSWORD>


def insert_local_ssh_conn(cursor):
    sql = """
        INSERT INTO public."connection"
        (conn_id, conn_type, host, "schema", login, password, port, extra, is_encrypted, is_extra_encrypted)
        VALUES('local_ssh_default', 'ssh', '192.168.0.178', '', '{LOCAL_SSH_USER}', '{LOCAL_SSH_USER_PASSWORD}', 22, '', false, false);
        """.format(
            LOCAL_SSH_USER=LOCAL_SSH_USER,
            LOCAL_SSH_USER_PASSWORD=LOCAL_SSH_USER_PASSWORD
            )
    cursor.execute(sql)

### connect to postgres instance in docker-compose via host=postgres
conn_string = "host='postgres' dbname='airflow' user='airflow' password='airflow'"
conn = psycopg2.connect(conn_string)
conn.autocommit = True
cursor = conn.cursor()
print('Inserting local ssh conn')
insert_local_ssh_conn(cursor)
```

### Ref
- official docker build example
	- https://airflow.apache.org/docs/apache-airflow/stable/production-deployment.html