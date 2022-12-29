#!/usr/bin/env python3
import click
from spaceone.core.utils import load_yaml_from_file, load_json
from repository_mirror.conf.my_conf import get_config

__all__ = ['cli']

_help = """
Execute DB migration based on the {version}.py file located in the migration folder.\
 Users can manage version history for DB migration.\n
Example usages:\n
    migrate.py version [-f <config_yml_path>] [-d]\n
The contents included in config yml:\n
    - BATCH_SIZE (type: int)\n
        A number of rows to be sent as a batch to the database\n
    - DB_NAME_MAP (type: dict)\n
        This is used because the database name is different depending on the environment.\n
    - LOG_PATH\n
        default: ${HOME}/db_migration_log/{version}.log
"""


@click.group()
def cli():
    pass


# @click.command(help=_help)
@cli.command()
# @click.argument('file_path')
@click.option('-f', '--file', 'file_path', type=click.Path(exists=True), help='YAML file only')
def all_resources(file_path):
    print('yes')
    # module = __import__(f'src.sync_resource', fromlist=['run_sync_repo'])
    # getattr(module, 'run_sync_repo')(file_path)


@cli.command()
@click.argument('resource')
@click.option('-j', '--json-parameter', help='JSON parameter')
@click.option('-f', '--file-parameter', 'file_path', type=click.Path(exists=True), help='YAML file only')
@click.option('-o', '--output', default='yaml', help='Output format',
              type=click.Choice(['table', 'json', 'yaml']), show_default=True)
def sync(resource, json_parameter, file_path, output):
    """Execute a method to resource"""
    print(resource)
    params = _parse_parameter(file_path, json_parameter)
    _execute_resource(resource, params=params, output=output)


def _parse_parameter(file_parameter=None, json_parameter=None):
    if file_parameter:
        params = load_yaml_from_file(file_parameter)
    else:
        params = {}

    if json_parameter:
        json_params = load_json(json_parameter)
        params.update(json_params)

    return params


def _execute_resource(resource, params=None, output='yaml'):
    if params is None:
        params = {}
    print(params)

    config = get_config()
    print(config)


if __name__ == '__main__':
    sync()
