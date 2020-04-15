def get_prefix(config):
    if config['bot']['prefix']:
        return config['bot']['prefix']
    else:
        return '^'  # default
