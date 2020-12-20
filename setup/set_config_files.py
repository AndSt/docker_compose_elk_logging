import yaml
import json


def set_kibana_config():
    with open("kibana/config/kibana.yml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    with open("kibana/config/kibana_default.yml", "w") as f:
        yaml.dump(config, f)

    # set new password and values
    with open("setup/data/built_in_passwords.json", "r") as f:
        passwords = json.load(f)
        password = passwords.get("kibana_system")

    config['elasticsearch.username'] = 'kibana_system'
    config['elasticsearch.password'] = password

    with open("kibana/config/kibana.yml", "w") as f:
        yaml.dump(config, f)


def set_logstash_config():
    with open("logstash/config/logstash.yml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    with open("logstash/config/logstash.yml", "w") as f:
        yaml.dump(config, f)

    # set new password and values
    with open("setup/data/built_in_passwords.json", "r") as f:
        passwords = json.load(f)
        password = passwords.get("logstash_system")

    config['xpack.monitoring.elasticsearch.username'] = 'logstash_system'
    config['xpack.monitoring.elasticsearch.password'] = password

    with open("logstash/config/logstash.yml", "w") as f:
        yaml.dump(config, f)


def set_logstash_pipeline_config(user_name: str = "test_user", password: str = "test_password"):
    with open("logstash/pipeline/logstash.conf", "r") as f:
        config_old = f.readlines()

    config_new = []
    for line in config_old:
        new_line = line
        if 'user => "elastic"' in line:
            new_line = new_line.replace('user => "elastic"', f'user => "{user_name}"')
        if 'password => "changeme"' in line:
            new_line = new_line.replace('password => "changeme"', f'password => "{password}"')
        config_new.append(new_line)

    with open("logstash/pipeline/logstash_new.conf", "w") as f:
        f.writelines(config_new)


if __name__ == '__main__':
    set_logstash_pipeline_config()
