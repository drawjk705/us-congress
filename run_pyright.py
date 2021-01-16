import os
import re
from typing import Set

PYRIGHT_CMD = "pyright ."
MISSING_TYPESTUB_PATTERN = r'.*error: Stub file not found for "(.*)".*'


def run_pyright() -> None:
    """
    Find all missing typestubs, generate them,
    then run pyright
    """
    modulesMissingStubs: Set[str] = set()

    for line in os.popen(PYRIGHT_CMD).readlines():
        match = re.match(MISSING_TYPESTUB_PATTERN, line)
        if match:
            group = match.group(1)
            group = re.sub(r"\..*", "", group)
            modulesMissingStubs.add(group)

    for module in modulesMissingStubs:
        cmd = f"{PYRIGHT_CMD} --createstub {module}"
        print(cmd)
        os.system(cmd)

    print(PYRIGHT_CMD)
    os.system(PYRIGHT_CMD)


if __name__ == "__main__":
    run_pyright()
