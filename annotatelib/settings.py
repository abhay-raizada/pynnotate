def get_config_file(config_path):
    config = {}
    exec(open(config_path).read(), {}, config)
    return config.get("databases", config.get("DATABASES", {}))