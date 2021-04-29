from typing import Optional, TextIO
import pexpect
import re
from .errors import (
    LoginFailedError,
    InvalidCommandError,
    CommitFailedError,
)

OPE_MODE_PROMPT_PATTERN = re.compile(r'\$ ')
CONF_MODE_PROMPT_PATTERN = re.compile(r'# ')
INVALID_COMMAND_ERROR_PATTERN = re.compile(r'Invalid command:')
COMMIT_FAILED_ERROR_PATTERN = re.compile(r'Commit failed')


class VyosConnector:
    def __init__(
            self,
            host: str,
            login_name: Optional[str] = None,
            port: Optional[int] = None,
            identity_file: Optional[str] = None,
            logfile: Optional[TextIO] = None) -> None:
        self.child = pexpect.spawn(
            self._generate_ssh_command(host, login_name, port, identity_file),
            logfile=logfile,
            encoding='utf-8'
        )
        matched_index = self.child.expect(
            [OPE_MODE_PROMPT_PATTERN, pexpect.EOF])
        if matched_index == 1:
            raise LoginFailedError()

    def enter_conf_mode(self):
        self.child.sendline('conf')
        self.child.expect(CONF_MODE_PROMPT_PATTERN)

    def exit_ope_mode(self):
        self.child.sendline('exit')
        self.child.expect(pexpect.EOF)

    def exit_conf_mode(self):
        self.child.sendline('exit')
        self.child.expect(OPE_MODE_PROMPT_PATTERN)

    def run_conf_mode_command(self, command: str):
        self.child.sendline(command)
        matched_index = self.child.expect(
            [INVALID_COMMAND_ERROR_PATTERN, CONF_MODE_PROMPT_PATTERN])
        if matched_index == 0:
            self.child.expect(CONF_MODE_PROMPT_PATTERN)
            raise InvalidCommandError(command)

    def run_commit(self):
        self.child.sendline('commit')
        matched_index = self.child.expect(
            [COMMIT_FAILED_ERROR_PATTERN, CONF_MODE_PROMPT_PATTERN])
        if matched_index == 0:
            self.child.expect(CONF_MODE_PROMPT_PATTERN)
            raise CommitFailedError()

    def run_save(self):
        self.child.sendline('save')
        self.child.expect(CONF_MODE_PROMPT_PATTERN)

    def run_exit_discard(self):
        self.child.sendline('exit discard')
        self.child.expect(OPE_MODE_PROMPT_PATTERN)

    def discard_then_exit(self):
        self.run_exit_discard()
        self.exit_ope_mode()

    def save_then_exit(self):
        self.run_save()
        self.exit_conf_mode()
        self.exit_ope_mode()

    def _generate_ssh_command(
            self,
            host: str,
            login_name: Optional[str],
            port: Optional[int],
            identity_file: Optional[str]):
        return ''.join(
            ['ssh ',
             f'-l {login_name} ' if login_name else '',
             f'-p {port} ' if port else '',
             f'-i {identity_file} ' if identity_file else '',
             host]
        )
