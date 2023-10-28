import subprocess
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Output:
    args: Any
    data: str
    returncode: int

    def list(self) -> list[str]:
        return self.data.split("\n")

def cmd(command: str) -> Output:
    # if i try to capture stderr as well by doing stderr=subropcess.PIPE as well
    # or using capture_output=True, fzf is not shown in the terminal
    output = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    return Output(output.args, output.stdout.decode().strip(), output.returncode)