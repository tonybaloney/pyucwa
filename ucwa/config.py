import yaml


def load_config():
    config = {}
    with open("config.yml", "r") as yaml_f:
        config = yaml.load(yaml_f)
    return config