import copy
import json
import os

SQLITE = { 'sqlite3': { 'driver': 'sqlite'} }
MYSQL = { 'mysql': { 'driver': 'mysql'} }
POSTGRES = { 'postgres': { 'driver': 'postgres'}}
CONFIG_FILE = 'pynnotate.json'

def get_config_file(config_path, **kwargs):
    if not config_path:
        config_path = find_config()
        if not config_path:
            config_path = write_config(**kwargs)
    config = json.loads(open(config_path).read())
    return config

def get_config(db, db_name, db_host, db_user, db_password):
    insufficient_args_message = 'Insufficient Arguments: db_name, db, db_user, db_password'
    insufficient_args_sqlite_message = 'Insufficient Arguments: db_name, db'
    if not(db_name and db):
        raise Exception(insufficient_args_sqlite_message)
    if db == 'sqlite':
        config = copy.deepcopy(SQLITE)
        db_driver = 'sqlite3'
    if db == 'mysql':
        config = copy.deepcopy(MYSQL)
        db_driver = 'mysql'
        if not(db_host and db_user and db_password):
            raise Exception(insufficient_args_message)
        config[db_driver]['host'] = db_host
        config[db_driver]['user'] = db_user
        config[db_driver]['password'] = db_password
    if db == 'postgres':
        config = copy.deepcopy(POSTGRES)
        db_driver = 'postgres'
        if not(db_host and db_user and db_password):
            raise Exception(insufficient_args_message)
        config[db_driver]['host'] = db_host
        config[db_driver]['user'] = db_user
        config[db_driver]['password'] = db_password
    config[db_driver]['database'] = db_name
    return config

def write_config(**kwargs):
    with open(CONFIG_FILE, "w+") as _file:
        config = get_config(
            kwargs["db"], kwargs["db_name"], kwargs["db_host"],
            kwargs["db_user"], kwargs["db_password"])
        _file.write(json.dumps(config, indent = 4))
    return CONFIG_FILE


def find_config():
    if os.path.isfile(CONFIG_FILE):
        return CONFIG_FILE
