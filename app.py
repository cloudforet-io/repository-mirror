## !/usr/bin/env python3

import os
import copy

from google.protobuf.json_format import MessageToDict
from spaceone.core import pygrpc, utils
from conf import *


class RepositoryResources:

    def __init__(self, external_conf_path=None):
        if external_conf_path:
            config = utils.load_yaml_from_file(external_conf_path)
            self.api_key = config.get('api_key')
            self.endpoint = config.get('endpoints')
            self.installed_plugins = config.get('installed_plugins')
        else:
            self.api_key = os.getenv('API_KEY', API_KEY)
            self.endpoint = os.getenv('ENDPOINT', ENDPOINT)
            self.installed_plugins = os.getenv('INSTALLED_PLUGINS', INSTALLED_PLUGINS)
        self.client = None

    def create_marketplace_variables(self):
        repository_id = self._get_repository_id('Marketplace')

        schemas = self._list_schemas(repository_id)
        policies = self._list_policies(repository_id)
        plugins = self._list_plugins(repository_id)

        variables = {'var': {'schema': schemas,
                             'policy': policies,
                             'plugin': plugins}}

        utils.save_yaml_to_file(variables, 'repository_resources_vars.yml')

        # TODO: make sync file

        return variables

    def create_resources_to_local_repository(self, marketplace_variables):
        schemas = marketplace_variables['var']['schema']
        policies = marketplace_variables['var']['policy']
        plugins = marketplace_variables['var']['plugin']

        self._create_schemas(schemas)
        # self._create_policies(policies)

        if self.installed_plugins:
            self._create_installed_plugins(plugins)
        else:
            self._create_plugins(plugins)

    def delete_resources_to_local_repository(self):
        repository_id = self._get_repository_id('Local')
        self._delete_schemas(repository_id)
        self._delete_plugins(repository_id)

    def _create_schemas(self, schemas):
        for schema in schemas:
            params = copy.deepcopy(schema)
            self.client.Schema.create(params, metadata=self._get_metadata())

    def _create_policies(self, policies):
        for policy in policies:
            params = copy.deepcopy(policy)
            self.client.Policy.create(params, metadata=self._get_metadata())

    def _create_installed_plugins(self, plugins):
        for plugin in plugins:
            image_repo, image_name = plugin['image'].split('/')
            if image_name in self.installed_plugins:
                params = copy.deepcopy(plugin)
                self.client.Plugin.register(params, metadata=self._get_metadata())

    def _create_plugins(self, plugins):
        for plugin in plugins:
            params = copy.deepcopy(plugin)
            self.client.Plugin.register(params, metadata=self._get_metadata())

    def _delete_schemas(self, repository_id):
        schemas = self._list_schemas(repository_id, all_columns=True)
        for schema in schemas:
            params = {'name': schema['name']}
            self.client.Schema.delete(params, metadata=self._get_metadata())

    def _delete_plugins(self, repository_id):
        plugins = self._list_plugins(repository_id, all_columns=True)
        for plugin in plugins:
            params = {'plugin_id': plugin['plugin_id']}
            self.client.Plugin.deregister(params, metadata=self._get_metadata())

    def _get_repository_id(self, target):
        repository_id = ''
        response = self._list_repositories(params={})
        for repository_info in response.get('results', []):
            if repository_info['name'] == target:
                repository_id = repository_info['repository_id']
        return repository_id

    def _list_repositories(self, params=None):
        self.client = self._get_client('repository')
        message = self.client.Repository.list(params or {}, metadata=self._get_metadata())
        return self._change_message(message)

    def _list_schemas(self, repository_id, all_columns=False):
        only = ['name', 'schema', 'service_type', 'labels', 'tags']
        params = {'repository_id': repository_id}
        message = self.client.Schema.list(params, metadata=self._get_metadata())
        schemas = self._change_message(message).get('results', [])
        if all_columns:
            return schemas
        else:
            return self.drop_keys(schemas, only)

    def _list_policies(self, repository_id, all_columns=False):
        only = ['labels', 'name', 'permissions', 'policy_id', 'tags']
        params = {'repository_id': repository_id}
        message = self.client.Policy.list(params, metadata=self._get_metadata())
        polices = self._change_message(message).get('results', [])
        if all_columns:
            return polices
        else:
            return self.drop_keys(polices, only)

    def _list_plugins(self, repository_id, all_columns=False):
        only = ['template', 'registry_type', 'tags', 'labels',
                'service_type', 'capability', 'name', 'provider', 'image']
        params = {
            'repository_id': repository_id,
            # 'query': {'only': only}
        }
        message = self.client.Plugin.list(params, metadata=self._get_metadata())
        plugins = self._change_message(message).get('results', [])

        if all_columns:
            return plugins
        else:
            return self.drop_keys(plugins, only)

    @staticmethod
    def drop_keys(resources, only):
        resources_only_keys = []
        for resource in resources:
            resource_keys = resource.keys()
            drop_keys = list(resource_keys - only)
            for key in drop_keys:
                resource.pop(key)
            resources_only_keys.append(resource)
        return resources_only_keys

    def _get_client(self, service):
        e = utils.parse_grpc_endpoint(self.endpoint[service])
        return pygrpc.client(endpoint=e['endpoint'], ssl_enabled=e['ssl_enabled'])

    @staticmethod
    def _change_message(message):
        return MessageToDict(message, preserving_proto_field_name=True)

    def _get_metadata(self):
        return (('token', self.api_key),)


if __name__ == '__main__':
    external_conf_path = '/Users/seolmin/.spaceone/environments/marketplace-contents.yml'
    repository = RepositoryResources(external_conf_path=external_conf_path)
    variables = repository.create_marketplace_variables()

    repository.create_resources_to_local_repository(variables)
    # repository.delete_resources_to_local_repository()
