#!/usr/bin/env python3

import os
import sys
import click
import traceback

try:
    import repository_mirror
except Exception:
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if path not in sys.path:
        sys.path.append(path)
from repository_mirror.command import sync, config

_DEBUG = os.environ.get('SPACECTL_DEBUG', 'false')

_HELP = """
Tools used to sync the repository.\n
Reference of repository concept:\n
https://spaceone-dev.gitbook.io/spaceone-apis\n
Following steps for first time user.\n
    1. repository-mirror config init\n
    2. repository-mirror config target api-key upsert <api_key>\n
    3. repository-mirror config target endpoint upsert <endpoint>\n
If you use spacectl's api_key and repository's endpoint\n
    1. repository-mirror config init\n
    2. repsoitory-mirror config target spacectl set <environment>
"""

cli = click.CommandCollection(sources=[config.cli, sync.cli], help=_HELP)


def main():
    try:
        cli(prog_name='repository_mirror')
    except Exception as e:
        click.echo(f'ERROR: {e}')
        click.echo()

        if _DEBUG.lower() == 'true':
            click.echo(traceback.format_exc())


if __name__ == '__main__':
    main()
