import os
from dataclasses import dataclass

from environs import Env


@dataclass
class Hidden:
    db_username: str
    db_password: str
    db_local_port: int
    db_name: str
    links: list
    old_db: str


def load_hidden_vars(path: str):
    env = Env()
    env.read_env()
    links = list()
    with open(os.path.dirname(os.path.abspath(__file__)) + '/path_links.txt', 'r') as path_links_file:
        for line in path_links_file:
            links.append(line.strip())

    return Hidden(
        db_username=env.str("DB_USERNAME"),
        db_password=env.str("DB_PASSWORD"),
        db_local_port=env.int("DB_LOCAL_PORT"),
        db_name=env.str("DB_NAME"),
        links=links,
        old_db=env.str("OLD_DB")
    )


hidden = load_hidden_vars(path='.env')
