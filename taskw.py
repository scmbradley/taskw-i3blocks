#!/usr/bin/python3

import subprocess
import json
import os


def _default(name, default="", arg_type=str):
    val = default
    if name in os.environ:
        val = os.environ[name]
    return arg_type(val)


strbool = lambda s: s.lower() in ["t", "true", "1"]


# I don't know who originally wrote these functions,
# but many of the python blocklets in i3blocks-contrib use it.

# arch-update added this code on 25 March 2018 and as far as I can tell
# this was the earliest use.


maxlen = _default("TASKW_MAX_LENGTH", default=35, arg_type=int)
notask_msg = _default("TASKW_NOTASK_MSG", default="No Task", arg_type=str)


def shorten(string):
    if len(string) <= maxlen:
        return string
    else:
        return string[: maxlen - 3] + "..."


def main():
    shell_cmd = "task +ACTIVE export"
    prcs = subprocess.check_output(shell_cmd, shell=True)
    j = json.loads(prcs)

    if len(j) == 0:
        bar_text = notask_msg
    elif len(j) == 1:
        bar_text = shorten(j[0]["description"])
    else:
        bar_text = shorten(j[0]["description"]) + " + " + str(len(j) - 1)
    return bar_text


if __name__ == "__main__":
    print(main())
