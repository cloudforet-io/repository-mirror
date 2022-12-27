## !/usr/bin/env python3

import sys
import click
import csv
import traceback
import json
import os
import pprint

from google.protobuf.json_format import MessageToDict
from spaceone.core import pygrpc, utils
from conf import API_KEY, ENDPOINT


class RepositoryResources:

    def __init__(self, external_conf_path=None):
        if external_conf_path:
            config = utils.load_yaml_from_file(external_conf_path)
            self.api_key = config.get('api_key')
            self.endpoint = config.get('endpoints')
        else:
            self.api_key = os.getenv('API_KEY', API_KEY)
            self.endpoint = os.getenv('ENDPOINT', ENDPOINT)
        self.client = None

    def create_marketplace_variables(self):
        repository_id = self._get_marketplace_repository_id()

        schemas = self._list_schemas(repository_id)
        polices = self._list_policies(repository_id)
        plugins = self._list_plugins(repository_id)

        variables = {'var': {'schema': schemas,
                             'policy': polices,
                             'plugin': plugins}}

        utils.save_yaml_to_file(variables, 'repository_resources_vars.yml')

        # TODO: make sync file

        return variables

    def create_resources_to_local_repository(self):
        pass

    def _get_marketplace_repository_id(self):
        repository_id = ''
        response = self._list_repositories(params={})
        for repository_info in response.get('results', []):
            if repository_info['name'] == 'Marketplace':
                repository_id = repository_info['repository_id']
        return repository_id

    def _list_repositories(self, params=None):
        self.client = self._get_client('repository')
        message = self.client.Repository.list(params or {}, metadata=self._get_metadata())
        return self._change_message(message)

    def _list_schemas(self, repository_id):
        only = ['name', 'schema', 'service_type', 'labels', 'tags']
        params = {'repository_id': repository_id}
        message = self.client.Schema.list(params, metadata=self._get_metadata())
        schemas = self._change_message(message).get('results', [])
        return self.drop_keys(schemas, only)

    def _list_policies(self, repository_id):
        only = ['labels', 'name', 'permissions', 'policy_id', 'tags']
        params = {'repository_id': repository_id}
        message = self.client.Policy.list(params, metadata=self._get_metadata())
        polices = self._change_message(message).get('results', [])
        return self.drop_keys(polices, only)

    def _list_plugins(self, repository_id):
        only = ['template', 'registry_type', 'tags', 'labels',
                'service_type', 'capability', 'name', 'provider', 'image']
        params = {
            'repository_id': repository_id,
            # 'query': {'only': only}
        }
        message = self.client.Plugin.list(params, metadata=self._get_metadata())
        plugins = self._change_message(message).get('results', [])

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
    external_conf_path = '/Users/seolmin/.spaceone/environments/dev.yml'
    repository = RepositoryResources(external_conf_path=external_conf_path)
    variables = repository.create_marketplace_variables()

    repository.create_resources_to_local_repository()
