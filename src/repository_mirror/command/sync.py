#!/usr/bin/env python3
import click
from spaceone.core.utils import load_yaml_from_file, load_json
from repository_mirror.conf.default_conf import *
from repository_mirror.conf.my_conf import *
from repository_mirror.manager.plugin_manager import PluginManager
from repository_mirror.manager.schema_manager import SchemaManager
from repository_mirror.manager.policy_manager import PolicyManager
from repository_mirror.manager.repository_manager import RepositoryManager

__all__ = ['cli']


@click.group()
def cli():
    pass


@cli.command()
@click.option('-j', '--json-parameter', help='JSON parameter')
@click.option('-f', '--file-parameter', 'file_path', type=click.Path(exists=True), help='YAML file only')
@click.option('-p', '--parameter', multiple=True, help='Input Parameter (-p <key>=<value> -p ...)')
@click.option('-o', '--output', default='yaml', help='Output format',
              type=click.Choice(['table', 'json', 'yaml']), show_default=True)
def sync(json_parameter, file_path, parameter, output):
    """Execute a method to resource"""
    config = _get_config_from_external(file_path, json_parameter, parameter)

    if not config:
        config = get_config()

    _check_config_key(config)
    _check_target(config)
    _check_resource_type(config)

    sync_plugins = config.get('SYNC_PLUGIN', SYNC_PLUGIN)
    sync_schemas = config.get('SYNC_SCHEMA', SYNC_SCHEMA)
    sync_policies = config.get('SYNC_POLICY', SYNC_POLICY)

    repository_manager = RepositoryManager(config)
    origin_repository_id = repository_manager.get_repository_id('remote')
    target_repository_id = repository_manager.get_repository_id('local')

    for resource_type in config['SYNC_RESOURCE_TYPE']:

        if resource_type == 'schema':
            schema_manager = SchemaManager(config)
            origin_schemas = schema_manager.list_schemas_from_origin({'repository_id': origin_repository_id})
            target_schemas = schema_manager.list_schemas_from_target({'repository_id': target_repository_id})
            origin_schema_names = [schema['name'] for schema in origin_schemas]
            target_schema_names = [schema['name'] for schema in target_schemas]
            schema_names_to_be_updated = _create_match_key_to_be_updated(origin_schema_names, target_schema_names)
            schema_names_to_be_created = _create_match_key_to_be_created(origin_schema_names, target_schema_names)

            if sync_schemas:
                for schema_name in schema_names_to_be_updated:
                    if schema_name not in sync_schemas:
                        schema_names_to_be_updated.remove(schema_name)

                for schema_name in schema_names_to_be_created:
                    if schema_name not in sync_schemas:
                        schema_names_to_be_updated.remove(schema_name)

            check_update_params = ['name', 'schema', 'labels', 'tags']
            check_create_params = ['name', 'schema', 'service_type', 'labels', 'tags']

            update_params_items = []
            for schema_name in schema_names_to_be_updated:
                origin_schema = [origin_schema for origin_schema in origin_schemas
                                 if origin_schema['name'] == schema_name]
                target_schema = [target_schema for target_schema in target_schemas
                                 if target_schema['name'] == schema_name]

                params = {'name': schema_name}
                for update_param in check_update_params:
                    if origin_schema[0][update_param] != target_schema[0][update_param]:
                        params.update({update_param: origin_schema[0][update_param]})
                if len(params.keys()) > 1:
                    update_params_items.append(params)

            for params in update_params_items:
                schema_manager.update_schema_from_target(params)

            for origin_schema in origin_schemas:
                if origin_schema['name'] in schema_names_to_be_created:
                    params = {}
                    for parameter in check_create_params:
                        params.update({parameter: origin_schema[parameter]})
                    schema_manager.create_schema_from_target(params)

        if resource_type == 'policy':
            policy_manager = PolicyManager(config)

        if resource_type == 'plugin':
            plugin_manager = PluginManager(config)


def _get_config_from_external(file_parameter=None, json_parameter=None, parameter=None):
    if file_parameter:
        params = load_yaml_from_file(file_parameter)
    else:
        params = {}

    if json_parameter:
        json_params = load_json(json_parameter)
        params.update(json_params)

    for p in parameter:
        p_split = p.split('=')
        if len(p_split) == 2:
            params[p_split[0]] = p_split[1]
        else:
            raise ValueError(f'Input parameter({p}) is invalid. (format: key=value)')

    return params


def _check_config_key(config):
    default_configs = set_default_config()
    for key in config.keys():
        if key not in default_configs.keys():
            raise Exception(f"Invalid config key (config keys:{list(config.keys())})")


def _check_resource_type(config):
    resource_types = config['SYNC_RESOURCE_TYPE']
    if not resource_types:
        raise Exception(f"At least one resource_type must be set. 'one of {SYNC_RESOURCE_TYPE}'")
    for resource_type in resource_types:
        if resource_type not in SYNC_RESOURCE_TYPE:
            raise Exception(f"resource_type must be included in one of {SYNC_RESOURCE_TYPE}.")


def _check_target(config):
    target = config['TARGET']
    target_api_key = target.get('API_KEY', TARGET.get('API_KEY'))
    target_endpoint = target.get('ENDPOINT', TARGET.get('ENDPOINT'))

    if not target_api_key:
        raise Exception(f"You need to set target's api_key in config first. (Use 'repository-mirror config')")
    if not target_endpoint:
        raise Exception(f"You need to set target's endpoint in config first. (Use 'repository-mirror config')")


def _create_match_key_to_be_updated(origin_items, target_items):
    match_keys = []
    for target_item in target_items:
        if target_item in origin_items:
            match_keys.append(target_item)
    return match_keys


def _create_match_key_to_be_created(origin_items, target_items):
    return list(set(origin_items) - set(target_items))


if __name__ == '__main__':
    sync()
