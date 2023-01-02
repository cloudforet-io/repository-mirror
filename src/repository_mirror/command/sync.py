#!/usr/bin/env python3
import click
import copy
from spaceone.core.utils import load_yaml_from_file, load_json
from repository_mirror.conf.default_conf import *
from repository_mirror.conf.my_conf import *
from repository_mirror.lib.output import echo
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
    """Synchronize TARGET with ORIGIN's repsitory' resources."""
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
                echo(f'[SYNC] SYNC_SCHEMA is set. ({sync_schemas})')
                schema_names_to_be_updated = _select_resources_from_sync_resource(schema_names_to_be_updated,
                                                                                  sync_schemas)
                schema_names_to_be_created = _select_resources_from_sync_resource(schema_names_to_be_created,
                                                                                  sync_schemas)
            else:
                echo(f"[SYNC] SYNC_SCHEMA is not set. Sync the entire schemas of ORIGIN.")

            schema_update_checklist = ['schema', 'labels', 'tags']
            schema_create_checklist = ['name', 'schema', 'service_type', 'labels', 'tags']

            update_schema_params = []
            create_schema_params = []
            if schema_names_to_be_updated:
                update_schema_params = _get_update_params_from_matched_resources(
                    primary_keys_to_be_updated=schema_names_to_be_updated,
                    origin_resources=origin_schemas,
                    target_resources=target_schemas,
                    update_checklist=schema_update_checklist,
                    match_key='name')

                for params in update_schema_params:
                    schema_manager.update_schema_from_target(params)
                    echo(f"[SYNC] {params['name']} has been updated.(update field:{list(params.keys())})")

            if schema_names_to_be_created:
                create_schema_params = _get_create_params_from_matched_resources(
                    primary_keys_to_be_created=schema_names_to_be_created, origin_resources=origin_schemas,
                    create_checklist=schema_create_checklist, match_key='name')

                for params in create_schema_params:
                    schema_manager.create_schema_from_target(params)
                    echo(f"[SYNC] {params['name']} has been created.")

            echo(f"[SYNC][RESULT] {len(update_schema_params)} schemas has been updated.")
            echo(f"[SYNC][RESULT] {len(create_schema_params)} schemas has been created.")
            echo(f"[SYNC][RESULT] ORIGIN has {len(origin_schemas)} schemas.")
            echo(f"[SYNC][RESULT] TARGET has {len(target_schemas) + len(create_schema_params)} schemas.")

        if resource_type == 'policy':
            policy_manager = PolicyManager(config)
            origin_polices = policy_manager.list_policies_from_origin({'repository_id': origin_repository_id})
            target_polices = policy_manager.list_policies_from_target({'repository_id': target_repository_id})
            origin_policy_ids = [policy['policy_id'] for policy in origin_polices]
            target_policy_ids = [policy['policy_id'] for policy in target_polices]
            policy_ids_to_be_updated = _create_match_key_to_be_updated(origin_policy_ids, target_policy_ids)
            policy_ids_to_be_created = _create_match_key_to_be_created(origin_policy_ids, target_policy_ids)

            if sync_policies:
                echo(f'[SYNC] SYNC_POLICY is set. ({sync_policies})')
                policy_ids_to_be_updated = _select_resources_from_sync_resource(policy_ids_to_be_updated,
                                                                                sync_policies)
                policy_ids_to_be_created = _select_resources_from_sync_resource(policy_ids_to_be_created,
                                                                                sync_policies)
            else:
                echo(f"[SYNC] SYNC_POLICY is not set. Sync the entire policies of ORIGIN.")

            policy_update_checklist = ['name', 'permissions', 'labels', 'tags']
            policy_create_checklist = ['policy_id', 'name', 'permissions', 'labels', 'tags']

            update_policy_params = []
            create_policy_params = []
            if policy_ids_to_be_updated:
                update_policy_params = _get_update_params_from_matched_resources(
                    primary_keys_to_be_updated=policy_ids_to_be_updated,
                    origin_resources=origin_polices,
                    target_resources=target_polices,
                    update_checklist=policy_update_checklist,
                    match_key='policy_id')

                for params in update_policy_params:
                    policy_manager.update_policy_from_target(params)
                    echo(f"[SYNC] {params['policy_id']} has been updated.(update field:{list(params.keys())})")

            if policy_ids_to_be_created:
                create_policy_params = _get_create_params_from_matched_resources(
                    primary_keys_to_be_created=policy_ids_to_be_created, origin_resources=origin_polices,
                    create_checklist=policy_create_checklist, match_key='policy_id')

                for params in create_policy_params:
                    policy_manager.create_policy_from_target(params)
                    echo(f"[SYNC] {params['policy_id']} has been created.")

            echo(f"[SYNC][RESULT] {len(update_policy_params)} policies has been updated.")
            echo(f"[SYNC][RESULT] {len(create_policy_params)} policies has been created.")
            echo(f"[SYNC][RESULT] ORIGIN has {len(origin_polices)} polices.")
            echo(f"[SYNC][RESULT] TARGET has {len(target_polices) + len(create_policy_params)} policies.")

        if resource_type == 'plugin':
            plugin_manager = PluginManager(config)
            origin_plugins = plugin_manager.list_plugins_from_origin({'repository_id': origin_repository_id})
            target_plugins = plugin_manager.list_plugins_from_target({'repository_id': target_repository_id})
            origin_plugin_images = [plugin['image'] for plugin in origin_plugins]
            target_plugin_images = [plugin['image'] for plugin in target_plugins]
            plugin_images_to_be_updated = _create_match_key_to_be_updated(origin_plugin_images, target_plugin_images)
            plugin_images_to_be_created = _create_match_key_to_be_created(origin_plugin_images, target_plugin_images)

            if sync_plugins:
                image_repo = 'pyengine'
                echo(f'[SYNC] SYNC_PLUGIN is set. ({sync_plugins})')
                sync_plugins = list(map(lambda x: image_repo + '/' + x, sync_plugins))
                plugin_images_to_be_updated = _select_resources_from_sync_resource(plugin_images_to_be_updated,
                                                                                   sync_plugins)
                plugin_images_to_be_created = _select_resources_from_sync_resource(plugin_images_to_be_created,
                                                                                   sync_plugins)
            else:
                echo(f"[SYNC] SYNC_PLUGIN is not set. Sync the entire plugins of ORIGIN.")

            plugin_update_checklist = ['name', 'capability', 'template', 'labels', 'tags']
            plugin_create_checklist = ['name', 'capability', 'template', 'registry_type',
                                       'service_type', 'provider', 'image', 'tags', 'labels']

            update_plugin_params = []
            create_plugin_params = []
            if plugin_images_to_be_updated:
                update_plugin_params = _get_update_params_from_matched_resources(
                    primary_keys_to_be_updated=plugin_images_to_be_updated,
                    origin_resources=origin_plugins,
                    target_resources=target_plugins,
                    update_checklist=plugin_update_checklist,
                    match_key='image')

                for params in update_plugin_params:
                    plugin_manager.update_plugin_from_target(params)
                    echo(f"[SYNC] {params['name']} has been updated.(update field:{list(params.keys())})")

            if plugin_images_to_be_created:
                create_plugin_params = _get_create_params_from_matched_resources(
                    primary_keys_to_be_created=plugin_images_to_be_created, origin_resources=origin_plugins,
                    create_checklist=plugin_create_checklist, match_key='image')

                for params in create_plugin_params:
                    plugin_manager.register_plugin_from_target(params)
                    echo(f"[SYNC] {params['name']} has been created.")

            echo(f"[SYNC][RESULT] {len(update_plugin_params)} plugins has been updated.")
            echo(f"[SYNC][RESULT] {len(create_plugin_params)} plugins has been created.")
            echo(f"[SYNC][RESULT] ORIGIN has {len(origin_plugins)} plugins.")
            echo(f"[SYNC][RESULT] TARGET has {len(target_plugins) + len(create_plugin_params)} plugins.")


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


def _select_resources_from_sync_resource(primary_key_resources, sync_resources):
    key_resources = copy.deepcopy(primary_key_resources)
    for key_resource in primary_key_resources:
        if key_resource not in sync_resources:
            key_resources.remove(key_resource)
    return key_resources


def _get_update_params_from_matched_resources(primary_keys_to_be_updated, origin_resources, target_resources,
                                              update_checklist, match_key, plugin=False):
    update_params_items = []
    for primary_key in primary_keys_to_be_updated:
        matched_origin_resource = [origin_resource for origin_resource in origin_resources
                                   if origin_resource[match_key] == primary_key]
        matched_target_resource = [target_resource for target_resource in target_resources
                                   if target_resource[match_key] == primary_key]
        if not plugin:
            params = {match_key: primary_key}
        else:
            params = {}

        for update_param in update_checklist:
            if matched_origin_resource[0][update_param] != matched_target_resource[0][update_param]:
                params.update({update_param: matched_origin_resource[0][update_param]})
        if len(params.keys()) > 1:
            update_params_items.append(params)
    return update_params_items


def _get_create_params_from_matched_resources(primary_keys_to_be_created, origin_resources, create_checklist,
                                              match_key):
    update_params = []
    for origin_resource in origin_resources:
        if origin_resource[match_key] in primary_keys_to_be_created:
            params = {}
            for parameter in create_checklist:
                if parameter in origin_resource.keys():
                    params.update({parameter: origin_resource[parameter]})
            update_params.append(params)
    return update_params


if __name__ == '__main__':
    sync()
