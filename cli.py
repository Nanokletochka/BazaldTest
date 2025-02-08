import click
from json import dumps
from module import *


@click.group()
def cli():
    """CLI utility for comparing binary packages."""

    pass


@cli.command()
@click.argument('branch1')
@click.argument('branch2')
@click.option(
    '--limit', type=int, default=None, help='Limit the number of packages for comparison.'
)
def existing(branch1, branch2, limit):
    """Compare existing packages between two branches."""

    pkg_1_json = get_packages(branch1)
    pkg_2_json = get_packages(branch2)
    result = compare_existing(pkg_1_json, pkg_2_json, limit)
    click.echo("=============== RESULTS ==============")
    click.echo(dumps(result, indent=4))
    click.echo("=============== END ==============")


@cli.command()
@click.argument('branch1')
@click.argument('branch2')
@click.option(
    '--limit', type=int, default=None, help='Limit the number of packages for comparison.'
)
def rpm(branch1, branch2, limit):
    """Compare RPM packages between two branches."""

    pkg_1_json = get_packages(branch1)
    pkg_2_json = get_packages(branch2)
    result = compare_rpm(pkg_1_json, pkg_2_json, limit)
    click.echo("=============== RESULTS ==============")
    click.echo(dumps(result, indent=4))
    click.echo("=============== END ==============")


if __name__ == '__main__':
    cli()
