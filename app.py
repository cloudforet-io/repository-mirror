#!/usr/bin/env python3

import sys
import click
import csv
import traceback
import json
import pprint

from google.protobuf.json_format import MessageToDict
from spaceone.core import pygrpc, utils

API_KEY = '<API_TOKEN>'

ENDPOINT = {
    'REPOSITORY': 'grpc+ssl://xxxxx.dev.spaceone.dev:443/v1',
}


def _change_message(message):
    return MessageToDict(message, preserving_proto_field_name=True)


def _get_metadata():
    return (('token', API_KEY),)


def _get_client(service):
    e = utils.parse_grpc_endpoint(ENDPOINT[service])
    return pygrpc.client(endpoint=e['endpoint'], ssl_enabled=e['ssl_enabled'])


def list_repositories(params=None):
    client = _get_client('REPOSITORY')
    message = client.Repository.list(params or {}, metadata=_get_metadata())
    return _change_message(message)


if __name__ == '__main__':
    params = {}
    response = list_repositories(params)
    for server_info in response.get('results', []):
        pprint.pprint(server_info)
