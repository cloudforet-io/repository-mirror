import click
from repository_mirror.lib.output import print_data
from repository_mirror.conf.global_conf import DEFAULT_ENVIRONMENT
from repository_mirror.conf.my_conf import *

__all__ = ['cli']


@click.group()
def cli():
    pass


@cli.group()
def config():
    """Modify repository-mirror config files"""
    pass


@config.command()
@click.option('-e', '--environment', prompt='Environment', help='Environment', default=DEFAULT_ENVIRONMENT)
@click.option('-f', '--import-file', type=click.Path(exists=True), help='YAML file only')
def init(environment, import_file):
    """Initialize repository-mirror config"""
    set_environment(environment)

    if import_file:
        import_config(import_file, environment)
    else:
        set_config({}, environment)


@config.command()
@click.argument('key')
@click.argument('value')
def set(key, value):
    """Set specific spaceconfig"""
    data = get_config()
    data[key] = value
    set_config(data)


@config.command()
@click.argument('key')
def remove(key):
    """Remove specific repository-mirror config"""
    data = get_config()

    if key in data:
        del data[key]

    set_config(data)


@config.command()
@click.option('-s', '--switch', help='Switch the environment')
@click.option('-r', '--remove', help='Remove the environment')
def environment(switch, remove):
    """Manage environments"""

    if switch:
        environments = list_environments()
        if switch not in environments:
            raise Exception(f"'{switch}' environment not found.")

        set_environment(switch)
        click.echo(f"Switched to '{switch}' environment.")
    elif remove:
        environments = list_environments()
        if remove not in environments:
            raise Exception(f"'{switch}' environment not found.")

        remove_environment(remove)
        click.echo(f"'{remove}' environment has been removed.")
    else:
        try:
            current_env = get_environment()
        except Exception:
            current_env = None

        environments = list_environments()
        if len(environments) == 0:
            raise Exception('config is undefined. (Use "spacectl config init")')

        for env in environments:
            if current_env == env:
                click.echo(f'{env} (current)')
            else:
                click.echo(env)


@config.command()
@click.option('-o', '--output', default='yaml', help='Output format',
              type=click.Choice(['json', 'yaml']), show_default=True)
def show(output):
    """Display a repository-mirror config"""
    data = get_config()
    print_data(data, output)


@config.group()
def plugin():
    """Manage plugins to be synced."""
    pass


@plugin.command()
@click.argument('plugin_id')
def add(plugin_id):
    """Add a specific plugin"""
    try:
        plugins = get_resource('sync_plugins')
    except Exception:
        plugins = []

    if plugin_id in plugins:
        raise ValueError(f"'{plugin_id}' already exists.")
    plugins.append(plugin_id)

    set_resource('sync_plugins', plugins)
    click.echo(f"'{plugin_id}' has been added.")


@plugin.command()
@click.argument('plugin_id')
def remove(plugin_id):
    """Remove a specific plugin"""
    remove_resource('sync_plugins', plugin_id)
    click.echo(f"'{plugin_id}' endpoint has been removed.")


@plugin.command()
@click.option('-o', '--output', default='table', help='Output format',
              type=click.Choice(['table', 'json', 'yaml']), show_default=True)
def show(output):
    """Display plugins"""
    plugins = list_resources('sync_plugins')
    print_data(plugins, output, headers=['sync_plugins'])


@config.group()
def schema():
    """Manage schemas to be synced."""
    pass


@schema.command()
@click.argument('schema_name')
def add(schema_name):
    """Add a specific schema"""
    try:
        schemas = get_resource('sync_schemas')
    except Exception:
        schemas = []

    if schema_name in schemas:
        raise ValueError(f"'{schema_name}' already exists.")
    schemas.append(schema_name)

    set_resource('sync_schemas', schemas)
    click.echo(f"'{schema_name}' schema has been added.")


@schema.command()
@click.argument('schema_name')
def remove(schema_name):
    """Remove a specific schema"""
    remove_resource('sync_schemas', schema_name)
    click.echo(f"'{schema_name}' schema has been removed.")


@schema.command()
@click.option('-o', '--output', default='table', help='Output format',
              type=click.Choice(['table', 'json', 'yaml']), show_default=True)
def show(output):
    """Display schemas"""
    schemas = list_resources('sync_schemas')
    print_data(schemas, output, headers=['sync_schemas'])


@config.group()
def policy():
    """Manage schemas to be synced."""
    pass


@policy.command()
@click.argument('policy_id')
def add(policy_id):
    """Add a specific policy"""
    try:
        policies = get_resource('sync_policies')
    except Exception:
        policies = []

    if policy_id in policies:
        raise ValueError(f"'{policy_id}' already exists.")
    policies.append(policy_id)

    set_resource('sync_policies', policies)
    click.echo(f"'{policy_id}' policy has been added.")


@policy.command()
@click.argument('policy_id')
def remove(policy_id):
    """Remove a specific policy"""
    remove_resource('sync_policies', policy_id)
    click.echo(f"'{policy_id}' policy has been removed.")


@policy.command()
@click.option('-o', '--output', default='table', help='Output format',
              type=click.Choice(['table', 'json', 'yaml']), show_default=True)
def show(output):
    """Display policies"""
    policies = list_resources('sync_policies')
    print_data(policies, output, headers=['sync_policies'])
