class VyosConnectorError(Exception):
    pass


class LoginFailedError(VyosConnectorError):
    pass


class ConfModeCommandFailedError(VyosConnectorError):
    pass


class InvalidCommandError(ConfModeCommandFailedError):
    pass


class CommitFailedError(ConfModeCommandFailedError):
    pass
