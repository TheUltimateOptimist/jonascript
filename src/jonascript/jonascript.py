import subprocess
from dataclasses import dataclass
from typing import Any, Union

@dataclass(frozen=True)
class Output:
    args: Any
    data: str
    returncode: int

    def list(self) -> list[str]:
        return self.data.split("\n")

def _cmd(command: Union[str, 'Command'], show_output: bool) -> Output:
    # if i try to capture stderr as well by doing stderr=subropcess.PIPE as well
    # or using capture_output=True, fzf is not shown in the terminal
    output = subprocess.run(command.command if type(command) is Command else command, shell=True, stdout=subprocess.PIPE)
    if show_output:
        print(output.stdout.decode())
    return Output(output.args, output.stdout.decode().strip(), output.returncode)

def cmd(command: Union[str, 'Command']) -> Output:
    return _cmd(command, False)

def cmdp(command: Union[str, 'Command']) -> Output:
    return _cmd(command, True)

@dataclass(frozen=True)
class Command:
    command: str

    def aand(self, command: str) -> 'Command':
        return Command(f"{self.command} && {command}")

    def oor(self, command: str) -> 'Command':
        return Command(f"{self.command} || {command}")

    def pipe(self, command: str) -> 'Command':
        return Command(f"{self.command} | {command}")

    def exec(self) -> Output:
        return cmd(self)

    def execp(self) -> Output:
        return cmdp(self)


HOME = cmd("echo $HOME").data
"""
equivalent to bash's $HOME, e.g. '/home/dev'
"""

WINDOW = Command("xprop -root")\
    .pipe("awk 'NR==1{print $NF}'")\
    .exec()\
    .data
"""
id of the focused window, e.g. '0x2000001'
"""