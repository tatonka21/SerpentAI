from serpent.game_launcher import GameLauncher, GameLauncherException
from serpent.utilities import is_linux, is_macos, is_windows

import shlex
import subprocess
from security import safe_command


class ExecutableGameLauncher(GameLauncher):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def launch(self, **kwargs):
        executable_path = kwargs.get("executable_path")

        if executable_path is None:
            raise GameLauncherException("An 'executable_path' kwarg is required...")

        if is_linux():
            safe_command.run(subprocess.Popen, shlex.split(executable_path))
        elif is_macos():
            safe_command.run(subprocess.Popen, shlex.split(executable_path))
        elif is_windows():
            safe_command.run(subprocess.Popen, shlex.split(executable_path))
