import json
import logging

from setup.config_logging import set_logging
from setup.manage_users import change_password
from setup.set_config_files import set_kibana_config, set_logstash_config


def setup_built_in_users():
    logging.info("Setup built-in users.")
    built_in_users = [
        'elastic',
        'apm_system',
        'kibana_system', 'kibana',
        'logstash_system',
        'beats_system',
        'remote_monitoring_user'
    ]
    user_pw_dict = {}
    for user in built_in_users:
        update = change_password(user)
        user_pw_dict.update(update)
    with open("setup/data/built_in_passwords.json", "w") as f:
        json.dump(user_pw_dict, f)

    logging.info("Setup kibana, logstash config.yml files.")
    set_kibana_config()
    set_logstash_config()

    logging.info("Restart kibana, logstash services")


if __name__ == '__main__':
    set_logging()

    logging.info("Setup built-in users.")
    setup_built_in_users()
