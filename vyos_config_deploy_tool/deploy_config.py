from typing import Optional, Iterable, TextIO
from vyos_config_deploy_tool.utils.vyos_connector import (
    VyosConnector,
    LoginFailedError,
    ConfModeCommandFailedError,
)


class ConfigDeployFailedError(Exception):
    pass


def deploy_config(
        commands: Iterable[str],
        host: str,
        login_name: Optional[str] = None,
        port: Optional[int] = None,
        identity_file: Optional[str] = None,
        logfile: Optional[TextIO] = None):
    try:
        vyos = VyosConnector(
            host=host,
            login_name=login_name,
            port=port,
            identity_file=identity_file,
            logfile=logfile
        )

        vyos.enter_conf_mode()
        vyos.load_default_config()

        for command in commands:
            vyos.run_conf_mode_command(command.strip())

        vyos.run_commit()
    except LoginFailedError:
        raise ConfigDeployFailedError()
    except ConfModeCommandFailedError:
        vyos.discard_then_exit()
        raise ConfigDeployFailedError()
    else:
        vyos.save_then_exit()
