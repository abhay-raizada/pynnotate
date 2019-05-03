import copy

def get_config_file(config_path):
    config = {}
    exec(open(config_path).read(), {}, config)
    print(config)
    print(config.get("databases", config.get("DATABASES", {})))
    return config.get("databases", config.get("DATABASES", {}))

def get_config(db_name, db, db_host, db_user, db_password):
    SQLITE = { 'sqlite3': { 'driver': 'sqlite'} }
    MYSQL = { 'mysql': { 'driver': 'mysql'} }
    POSTGRES = { 'postgres': { 'driver': 'postgres'}}
    if db == 'sqlite':
        config = copy.deepcopy(SQLITE)
        db_driver = 'sqlite3'
    if db == 'mysql':
        config = copy.deepcopy(MYSQL)
        db_driver = 'mysql'
        config[db_driver]['host'] = db_host
        config[db_driver]['user'] = db_user
        config[db_driver]['password'] = db_password
    if db == 'postgres':
        config = copy.deepcopy(POSTGRES)
        db_driver = 'postgres'
        config[db_driver]['host'] = db_host
        config[db_driver]['user'] = db_user
        config[db_driver]['password'] = db_password
    config[db_driver]['database'] = db_name

    print(config)
    return config
    #return {'sqlite3': {'driver': 'sqlite', 'database': 'test.db'}}