#!/usr/bin/python3

import subprocess
import json
import os


def _default(name, default="", arg_type=str):
    val = default
    if name in os.environ:
        val = os.environ[name]
    return arg_type(val)


def strbool(s):
    return s.lower() in ["t", "true", "1"]


# I don't know who originally wrote these functions,
# but many of the python blocklets in i3blocks-contrib use it.

# arch-update added this code on 25 March 2018 and as far as I can tell
# this was the earliest use.


maxlen = _default("TASKW_MAX_LENGTH", default=35, arg_type=int)
notask_msg = _default("TASKW_NOTASK_MSG", default="No Task", arg_type=str)
urgency_bool = _default("TASKW_SORT_URGENCY", default="", arg_type=strbool)


taskw_tf = _default("TASKW_TF", default="t", arg_type=strbool)
timew_tf = _default("TIMEW_TF", default="f", arg_type=strbool)
timew_desc_override = _default("TIMEW_DESC_OVERRIDE", default="f", arg_type=strbool)

# Set timew_tf to true if the override is set.
if timew_desc_override:
    timew_tf = True

##############################
# TESTING TESTING TESTING

# taskw_tf = False
# timew_desc_override = True
##############################


def shorten(string):
    if len(string) <= maxlen:
        return string
    else:
        return string[: maxlen - 3] + "..."


def export_taskw():
    shell_cmd = "task +ACTIVE export"
    j = json.loads(subprocess.check_output(shell_cmd, shell=True))
    max_urg = 0
    if len(j) > 0:
        if urgency_bool:
            for i in range(len(j)):
                if j[i]["urgency"] > j[max_urg]["urgency"]:
                    max_urg = i
        return j[max_urg]["description"], len(j)
    else:
        return notask_msg, 0


def export_timew_text():
    timew_shell = "timew get dom.active.tag.1"
    # the output of `timew get` includes a newline that we have to strip.
    timew_txt = subprocess.check_output(timew_shell, shell=True).decode("utf-8")[:-1]
    return timew_txt


def export_timew_active():
    timew_active_shell = "timew get dom.active"
    timew_active_tf = subprocess.check_output(timew_active_shell, shell=True)
    return True if b"1" in timew_active_tf else False


def main():
    task_desc = ""
    task_append = ""
    if taskw_tf:
        descr, task_num = export_taskw()
        task_desc = shorten(descr)
        if task_num > 1:
            task_append = " + " + str(task_num - 1)

    if timew_tf:
        # pull duration
        pass

    if timew_desc_override or not taskw_tf:
        task_desc = (
            shorten(export_timew_text()) if export_timew_active() else notask_msg
        )
    # We will be appending more things to this, later.
    bar_text = task_desc + task_append
    return bar_text


if __name__ == "__main__":
    print(main())
