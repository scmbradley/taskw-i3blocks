#!/usr/bin/python3

# from tasklib import TaskWarrior

import subprocess
import json
import os


def _default(name, default="", arg_type=str):
    val = default
    if name in os.environ:
        val = os.environ[name]
    return arg_type(val)


maxlen = _default("TASKW_MAX_LENGTH", default=35, arg_type=int)


def shorten(string):
    if len(string) <= maxlen:
        return string
    else:
        return string[:30] + "..."


def main():
    shell_cmd = "task +ACTIVE export"
    prcs = subprocess.run(shell_cmd, shell=True, capture_output=True)
    j = json.loads(prcs.stdout)

    if len(j) == 0:
        bar_text = "No task"
    elif len(j) == 1:
        bar_text = shorten(j[0]["description"])
    else:
        bar_text = shorten(j[0]["description"]) + " + " + str(len(j) - 1)
    return bar_text


if __name__ == "__main__":
    print(main())
