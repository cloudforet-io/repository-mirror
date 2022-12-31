from spaceone.core import pygrpc, utils
from repository_mirror.conf.default_conf import *
from google.protobuf.json_format import MessageToDict


class SpaceoneClient(object):

    def __init__(self, config):
        self.origin = config.get('ORIGIN', ORIGIN)
        self.origin_api_key = self.origin.get('API_KEY', ORIGIN.get('API_KEY'))
        self.origin_endpoint = self.origin.get('ENDPOINT', ORIGIN.get('ENDPOINT'))
        self.target = config.get('TARGET', TARGET)
        self.target_api_key = self.target.get('API_KEY', TARGET.get('API_KEY'))
        self.target_endpoint = self.target.get('ENDPOINT', TARGET.get('ENDPOINT'))
        self.sync_resource_types = config.get('SYNC_RESOURCE_TYPE', SYNC_RESOURCE_TYPE)
        self.sync_plugins = config.get('SYNC_PLUGIN', SYNC_PLUGIN)
        self.sync_schemas = config.get('SYNC_SCHEMA', SYNC_SCHEMA)
        self.sync_policies = config.get('SYNC_POLICY', SYNC_POLICY)

        self._check_target()

    def origin_client(self):
        e = utils.parse_grpc_endpoint(self.origin_endpoint)
        return pygrpc.client(endpoint=e['endpoint'], ssl_enabled=e['ssl_enabled'])

    def target_client(self):
        e = utils.parse_grpc_endpoint(self.target_endpoint)
        return pygrpc.client(endpoint=e['endpoint'], ssl_enabled=e['ssl_enabled'])

    @staticmethod
    def change_message(message):
        return MessageToDict(message, preserving_proto_field_name=True)

    def get_metadata(self):
        return (('token', self.target_api_key),)

    def _check_target(self):
        if not self.target_api_key:
            raise Exception(f"You need to set target's api_key in config first. (Use 'repository-mirror config')")
        if not self.target_endpoint:
            raise Exception(f"You need to set target's endpoint in config first. (Use 'repository-mirror config')")
