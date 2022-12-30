import os
from spaceone.core import utils
from repository_mirror.conf.global_conf import *
from repository_mirror.conf import default_conf


def get_config(key=None, default=None, environment=None):
    if environment is None:
        environment = get_environment()

    try:
        environment_path = os.path.join(ENVIRONMENT_DIR, f'{environment}.yml')
        data = utils.load_yaml_from_file(environment_path)
    except Exception:
        raise Exception('config is undefined. (Use "repository_mirror config init")')

    if key:
        return data.get(key, default)
    else:
        return data


def get_environment():
    try:
        data = utils.load_yaml_from_file(ENVIRONMENT_CONF_PATH)
    except Exception:
        raise Exception('config is undefined. (Use "repository_mirror config init")')

    environment = data.get('environment')

    return environment


def set_environment(environment):
    utils.create_dir(CONFIG_DIR)
    utils.create_dir(ENVIRONMENT_DIR)
    utils.save_yaml_to_file({'environment': environment}, ENVIRONMENT_CONF_PATH)


def import_config(import_file_path, environment=None):
    if environment is None:
        environment = get_environment()

    try:
        environment_path = os.path.join(ENVIRONMENT_DIR, f'{environment}.yml')
        data = utils.load_yaml_from_file(import_file_path)
        utils.save_yaml_to_file(data, environment_path)
    except Exception:
        raise Exception(f'Import file format is invalid. (file = {import_file_path})')


def set_config(new_data, environment=None):
    if environment is None:
        environment = get_environment()

    try:
        environment_path = os.path.join(ENVIRONMENT_DIR, f'{environment}.yml')
        utils.save_yaml_to_file(new_data, environment_path)
    except Exception:
        raise Exception('config is undefined. (Use "repository_mirror config init")')


def list_environments():
    environments = []
    try:
        for f in os.listdir(ENVIRONMENT_DIR):
            if os.path.isfile(os.path.join(ENVIRONMENT_DIR, f)) and f.find('.yml') > 1:
                environments.append(f.rsplit('.', 1)[0])
    except Exception:
        raise Exception('config is undefined. (Use "repository_mirror config init")')

    return environments


def remove_environment(environment):
    try:
        environment_path = os.path.join(ENVIRONMENT_DIR, f'{environment}.yml')
        if os.path.exists(environment_path):
            os.remove(environment_path)
    except Exception as e:
        raise Exception(f'Environment deletion error: {e}')

    environments = list_environments()
    if len(environments) > 0:
        utils.save_yaml_to_file({'environment': environments[0]}, ENVIRONMENT_CONF_PATH)
    else:
        os.remove(ENVIRONMENT_CONF_PATH)


def set_resource(key, resources, environment=None):
    data = get_config(environment)
    data[key] = resources

    set_config(data, environment)


def get_resource(resource_type, environment=None):
    plugins = get_config(resource_type, [], environment)
    return plugins


def remove_resource(key, resource, environment=None):
    data = get_config(environment)
    resources = data.get(key, [])

    if resource in resources:
        resources.remove(resource)
    else:
        raise Exception(f'{resource} is undefined ( {key}:{resources} )')

    data[key] = resources

    set_config(data, environment)


def list_resources(key, environment=None):
    resources = get_config(key, {}, environment)
    result = []

    for resource in resources:
        result.append((resource,))

    return result


def set_default_config():
    configs = {}
    for key in dir(default_conf):
        if not key.startswith('__'):
            configs.update({key: eval(f'default_conf.{key}')})
    return configs


def list_inner_resources(key, environment=None):
    resources = get_config(key, {}, environment)
    result = []

    for inner_key, item in resources.items():
        result.append((inner_key, item))

    return result


if __name__ == '__main__':
    set_default_config()
    # test()
