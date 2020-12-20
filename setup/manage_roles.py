from typing import Dict

from setup.utils import get_elk_security, post_elk_security


def is_same_role(data: Dict, role: Dict):
    if data.get("cluster") != role.get("cluster"):
        raise ValueError("Cluster settings don't match")

    if data.get("indices")[0].get("names") != role.get("indices")[0].get("names"):
        raise ValueError("Cluster settings don't match")
    if data.get("indices")[0].get("privileges") != role.get("indices")[0].get("privileges"):
        raise ValueError("Cluster settings don't match")
    return True


def create_logstash_role(role_name: str = "logstash_writer"):
    data = {
        "cluster": ["manage_index_templates", "monitor", "manage_ilm"],
        "indices": [
            {
                "names": ["logstash-*"],
                "privileges": ["write", "create", "delete", "create_index", "manage", "manage_ilm"]
            }
        ]
    }
    role = get_role(role_name)
    if role_name in role:
        return is_same_role(data, role.get(role_name))

    response = post_elk_security(f"role/{role_name}", data=data)
    if response.get("role", {}).get("created", False) is True:
        return True
    return False


def get_role(name: str) -> Dict:
    response = get_elk_security(f"role/{name}")
    return response


# , auth=("elastic", passwords.get("elastic")), verify=True
if __name__ == '__main__':
    print(create_logstash_role())
