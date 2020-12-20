from typing import List, Dict
import json

from setup.utils import get_elk_security, post_elk_security, generate_password


def get_user(user_name="kib_user") -> Dict:
    response = get_elk_security(f"user/{user_name}")
    return response


def is_same_user(data: Dict, user: Dict):
    if data.get("full_name") != user.get("full_name"):
        return False
    if data.get("roles") != user.get("roles"):
        return False
    return True


def create_user(user_name: str = "kibana_user", roles: List[str] = None):
    if roles is None:
        raise ValueError("Roles need to be provided")

    data = {
        "password": generate_password(),
        "roles": roles,
        "full_name": user_name
    }

    user = get_user(user_name)
    if user.get(user_name, None) is not None:
        user = user.get(user_name)
        if is_same_user(data, user):
            return data
        else:
            raise ValueError(f"There has an error with creation as of user: {user}")

    response = post_elk_security(url=f"user/{user_name}", data=data)
    if not response.get("created", False):
        raise ConnectionError(f"Error: {response}")
    return data


def change_password(user_name):
    password = generate_password()
    data = {
        "password": password
    }
    response = post_elk_security(url=f"user/{user_name}/_password", data=data)
    if response == {}:
        resp = dict()
        resp[user_name] = password
        if user_name == "elastic":
            with open("setup/data/elastic_password.json", "w") as f:
                json.dump(resp, f)
        return resp
    else:
        raise ConnectionError("Error")


if __name__ == '__main__':
    print(get_user("elastic"))
