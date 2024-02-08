from dataclasses import dataclass

from environs import Env


@dataclass
class Hidden:
    db_username: str
    db_password: str
    db_local_port: int
    db_name: str
    links: list


def load_hidden_vars(path: str):
    env = Env()
    env.read_env()
    links = list()
    with open('path_links.txt', 'r') as path_links_file:
        for line in path_links_file:
            links.append(line.strip())

    return Hidden(
        db_username=env.str("DB_USERNAME"),
        db_password=env.str("DB_PASSWORD"),
        db_local_port=env.int("DB_LOCAL_PORT"),
        db_name=env.str("DB_NAME"),
        links=links
    )


hidden = load_hidden_vars(path='.env')
