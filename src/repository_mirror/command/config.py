import click
from repository_mirror.lib.output import print_data
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
        default_configs = set_default_config()
        set_config(default_configs, environment)


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
            raise Exception('config is undefined. (Use "repository-mirror config init")')

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
        plugins = get_resource('SYNC_PLUGIN')
    except Exception:
        plugins = []

    if plugin_id in plugins:
        raise ValueError(f"'{plugin_id}' already exists.")
    plugins.append(plugin_id)

    set_resource('SYNC_PLUGIN', plugins)
    click.echo(f"'{plugin_id}' has been added.")


@plugin.command()
@click.argument('plugin_id')
def remove(plugin_id):
    """Remove a specific plugin"""
    remove_resource('SYNC_PLUGIN', plugin_id)
    click.echo(f"'{plugin_id}' endpoint has been removed.")


@plugin.command()
@click.option('-o', '--output', default='table', help='Output format',
              type=click.Choice(['table', 'json', 'yaml']), show_default=True)
def show(output):
    """Display plugins"""
    plugins = list_resources('SYNC_PLUGIN')
    print_data(plugins, output, headers=['sync_plugin'])


@config.group()
def schema():
    """Manage schemas to be synced."""
    pass


@schema.command()
@click.argument('schema_name')
def add(schema_name):
    """Add a specific schema"""
    try:
        schemas = get_resource('SYNC_SCHEMA')
    except Exception:
        schemas = []

    if schema_name in schemas:
        raise ValueError(f"'{schema_name}' already exists.")
    schemas.append(schema_name)

    set_resource('SYNC_SCHEMA', schemas)
    click.echo(f"'{schema_name}' schema has been added.")


@schema.command()
@click.argument('schema_name')
def remove(schema_name):
    """Remove a specific schema"""
    remove_resource('SYNC_SCHEMA', schema_name)
    click.echo(f"'{schema_name}' schema has been removed.")


@schema.command()
@click.option('-o', '--output', default='table', help='Output format',
              type=click.Choice(['table', 'json', 'yaml']), show_default=True)
def show(output):
    """Display schemas"""
    schemas = list_resources('SYNC_SCHEMA')
    print_data(schemas, output, headers=['sync_schema'])


@config.group()
def policy():
    """Manage schemas to be synced."""
    pass


@policy.command()
@click.argument('policy_id')
def add(policy_id):
    """Add a specific policy"""
    try:
        policies = get_resource('SYNC_POLICY')
    except Exception:
        policies = []

    if policy_id in policies:
        raise ValueError(f"'{policy_id}' already exists.")
    policies.append(policy_id)

    set_resource('SYNC_POLICY', policies)
    click.echo(f"'{policy_id}' policy has been added.")


@policy.command()
@click.argument('policy_id')
def remove(policy_id):
    """Remove a specific policy"""
    remove_resource('SYNC_POLICY', policy_id)
    click.echo(f"'{policy_id}' policy has been removed.")


@policy.command()
@click.option('-o', '--output', default='table', help='Output format',
              type=click.Choice(['table', 'json', 'yaml']), show_default=True)
def show(output):
    """Display policies"""
    policies = list_resources('SYNC_POLICY')
    print_data(policies, output, headers=['sync_policy'])


@config.group()
def resource_type():
    """
    Manage resource_type to be synced.\n
    Manage the resources corresponding to ['plugin', 'schema', 'policy']
    """
    pass


@resource_type.command()
@click.argument('resource_type')
def add(resource_type):
    """Add a specific resource_type"""
    try:
        resource_types = get_resource('SYNC_RESOURCE_TYPE')
    except Exception:
        resource_types = []

    if resource_type in resource_types:
        raise ValueError(f"'{resource_type}' already exists.")

    if resource_type not in MANAGED_RESOURCES:
        raise ValueError(f"'{resource_type}' invalid repository resources")

    resource_types.append(resource_type)

    set_resource('SYNC_RESOURCE_TYPE', resource_types)
    click.echo(f"'{resource_type}' resource_type has been added.")


@resource_type.command()
@click.argument('resource_type')
def remove(resource_type):
    """Remove a specific resource_type"""
    remove_resource('SYNC_RESOURCE_TYPE', resource_type)
    click.echo(f"'{resource_type}' resource_type has been removed.")


@resource_type.command()
@click.option('-o', '--output', default='table', help='Output format',
              type=click.Choice(['table', 'json', 'yaml']), show_default=True)
def show(output):
    """Display resource_types"""
    resource_types = list_resources('SYNC_RESOURCE_TYPE')
    print_data(resource_types, output, headers=['sync_resource_type'])


@config.group()
def origin():
    """
    Manage origin repository
    """
    pass


@origin.group()
def endpoint():
    """
    Manage endpoint of origin repository
    """
    pass


@endpoint.command()
@click.argument('endpoint')
def upsert(endpoint):
    """Add a specific endpoint"""
    try:
        origin_config = get_resource('ORIGIN')
    except Exception:
        origin_config = {}

    if endpoint == origin_config['ENDPOINT']:
        raise ValueError(f"'{endpoint}' already exists.")

    origin_config['ENDPOINT'] = endpoint

    set_resource('ORIGIN', origin_config)
    click.echo(f"'{endpoint}' endpoint has been added.")


@endpoint.command()
@click.option('-o', '--output', default='table', help='Output format',
              type=click.Choice(['table', 'json', 'yaml']), show_default=True)
def show(output):
    """Display endpoint of origin repository """
    resource_types = list_inner_resources('ORIGIN')
    print_data(resource_types, output, headers=['origin'])


@config.group()
def target():
    """
    Manage target repository
    """
    pass


@target.group()
def endpoint():
    """
    Manage endpoint of origin repository
    """
    pass


@target.group()
def api_key():
    """
    Manage api_key of origin repository
    """
    pass


@target.group()
def spacectl():
    """Add api_key and repository endpoint of spacectl"""
    pass


@endpoint.command()
@click.argument('endpoint')
def upsert(endpoint):
    """Add a specific endpoint"""
    try:
        origin_config = get_resource('TARGET')
    except Exception:
        origin_config = {}

    if endpoint == origin_config['ENDPOINT']:
        raise ValueError(f"'{endpoint}' already exists.")

    origin_config['ENDPOINT'] = endpoint

    set_resource('TARGET', origin_config)
    click.echo(f"'{endpoint}' endpoint has been added.")


@endpoint.command()
@click.option('-o', '--output', default='table', help='Output format',
              type=click.Choice(['table', 'json', 'yaml']), show_default=True)
def show(output):
    """Display endpoint of origin repository """
    resource_types = list_inner_resources('TARGET')
    print_data(resource_types, output, headers=['target'])


@api_key.command()
@click.argument('api_key')
def upsert(api_key):
    """Add a specific api_key"""
    try:
        origin_config = get_resource('TARGET')
    except Exception:
        origin_config = {}

    if api_key == origin_config['API_KEY']:
        raise ValueError(f"'{api_key}' already exists.")

    origin_config['API_KEY'] = api_key

    set_resource('TARGET', origin_config)
    click.echo(f"'{api_key}' api_key has been added.")


@api_key.command()
@click.option('-o', '--output', default='table', help='Output format',
              type=click.Choice(['table', 'json', 'yaml']), show_default=True)
def show(output):
    """Display api_key of origin repository """
    resource_types = list_inner_resources('TARGET')
    print_data(resource_types, output, headers=['target'])


@spacectl.command()
@click.argument('environment')
def set(environment):
    """Add a spacectl api_key"""
    try:
        origin_config = get_resource('TARGET')
    except Exception:
        origin_config = {}

    try:
        spacectl_environment_path = os.path.join(SPACECTL_ENVIRONMENT_DIR, f'{environment}.yml')
        data = utils.load_yaml_from_file(spacectl_environment_path)
    except Exception:
        raise Exception('config is undefined. (Use "spacectl config init")')

    api_key_from_spacectl = data.get('api_key', '')
    endpoint_from_spacectl = data.get('endpoints', {})

    if not endpoint_from_spacectl:
        raise Exception(f'Make sure the settings in that file are correct. ({spacectl_environment_path})')

    repository_endpoint_form_spacectl = endpoint_from_spacectl.get('repository', '')

    if not api_key_from_spacectl:
        raise Exception(f'Make sure the settings in that api_key are correct. ({spacectl_environment_path})')
    elif not repository_endpoint_form_spacectl:
        raise Exception(
            f'Make sure the settings in that repository endpoint are correct. ({spacectl_environment_path})')

    origin_config['API_KEY'] = api_key_from_spacectl
    origin_config['ENDPOINT'] = repository_endpoint_form_spacectl

    set_resource('TARGET', origin_config)
    click.echo(f"'spacectl api_key' has been added.")
    click.echo(f"'{repository_endpoint_form_spacectl}' endpoint has been added.")
