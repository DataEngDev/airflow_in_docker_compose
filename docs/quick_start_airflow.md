### Quick Start

1. Launch airflow via docker-compose
```bash
git clone https://github.com/DataEngDev/airflow_in_docker_compose.git
cd airflow_in_docker_compose

docker-compose -f docker-compose-2.0-with-celery-executor.yml up --buil

# account, password : admin, admin
```

2. Install py packages
```bash
docker ps -a 

#docker exec -it 56d9da22d7cf bash
docker exec -it <airflow_in_docker_compose_worker_1's id> bash

pip install --upgrade pip
pip install pywebhdfs
```


### Ref
- official docker build example
	- https://airflow.apache.org/docs/apache-airflow/stable/production-deployment.html