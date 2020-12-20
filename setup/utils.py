import os
from typing import Dict
import requests
import json
import secrets
import string


def generate_password(num_letters: int = 16) -> str:
    alphabet = string.ascii_letters + string.digits  # + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(num_letters))
    return password


def read_elastic_password(password_file: str = None) -> Dict:
    if password_file is None:
        password_file = "setup/data/elastic_password.json"
    if not os.path.isfile(password_file):
        raise ValueError(f"No password file {password_file} exists.")

    with open(password_file, "r") as f:
        password = json.load(f).get('elastic')
    return password


def get_elk_security(url: str) -> Dict:
    elastic_password = read_elastic_password()
    elastic_url = f'http://localhost:9200/_security/{url}'

    headers = {'Accept': 'application/json'}
    response = requests.get(elastic_url, auth=("elastic", elastic_password), verify=False, headers=headers)

    response = response.json()
    if "error" in response:
        raise ConnectionError(f"Error: {response}")

    return response


def post_elk_security(url: str, data: Dict = None) -> Dict:
    elastic_password = read_elastic_password()
    elastic_url = f'http://localhost:9200/_security/{url}'

    headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
    response = requests.post(
        elastic_url, data=json.dumps(data), auth=("elastic", elastic_password), verify=False, headers=headers
    )

    response = response.json()
    if "error" in response:
        raise ConnectionError(f"Error: {response}")

    return response
