#!/usr/bin/env bash

cd $ELK_REPO_BASE_DIR

docker-compose up -d --build
echo "ELK ontainers are built. Sleeping for 30 seconds"
sleep 30

# create system users
PYTHONPATH=. python setup/setup_built_in_users.py
docker-compose restart kibana logstash
echo "Logstash; Kibana are restarted. Sleeping for 30 seconds"
sleep 30

PYTHONPATH=. python setup/setup_actual_users.py

docker-compose restart kibana logstash
sleep 30

# TODO send dummy logging