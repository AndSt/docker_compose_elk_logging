import os
import logging
import json

from setup.config_logging import set_logging
from setup.manage_users import create_user
from setup.manage_roles import create_logstash_role
from setup.set_config_files import set_logstash_pipeline_config


def setup_actual_users():
    logging.info("Setup logstash role.")
    logstash_role = "logstash_writer"
    create_logstash_role(logstash_role)

    passwords = {}
    logging.info("Setup logstash user.")
    logstash_user = "logstash_writer"
    data = create_user(logstash_user, [logstash_role])
    passwords[logstash_user] = data

    logging.info("Setup logstash pipeline file.")
    print(passwords)
    set_logstash_pipeline_config(logstash_user, passwords.get(logstash_user).get("password"))

    logging.info("Setup kibana user.")
    kibana_user = os.getenv("KIBANA_USER", "kibana_user")
    data = create_user(kibana_user, ['kibana_admin'])

    passwords[kibana_user] = data

    with open("setup/data/user_passwords.json", "w") as f:
        json.dump(passwords, f)


if __name__ == '__main__':
    set_logging()
    setup_actual_users()
