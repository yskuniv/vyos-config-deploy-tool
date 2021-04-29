import click
import sys
from .deploy_config import (
    deploy_config,
    ConfigDeployFailedError,
)


@click.command()
@click.argument('config',
                type=click.File(),
                metavar='config')
@click.option('-h',
              'host',
              metavar='host',
              required=True)
@click.option('-l',
              'login_name',
              metavar='login_name')
@click.option('-p',
              'port',
              type=int,
              metavar='port')
@click.option('-i',
              'identity_file',
              type=click.Path(exists=True, dir_okay=False),
              metavar='identity_file')
@click.version_option()
def main(config, host, login_name, port, identity_file):
    commands = config.readlines()

    try:
        deploy_config(
            commands=commands,
            host=host,
            login_name=login_name,
            port=port,
            identity_file=identity_file,
            logfile=sys.stderr
        )
    except ConfigDeployFailedError:
        exit(1)
