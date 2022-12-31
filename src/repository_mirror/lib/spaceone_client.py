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
