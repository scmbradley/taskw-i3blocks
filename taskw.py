#!/usr/bin/python3

# This is taskw.py v0.2.2

import subprocess
import json
import os
import re


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
urgency_tf = _default("TASKW_SORT_URGENCY", default="f", arg_type=strbool)
taskw_tf = _default("TASKW_TF", default="t", arg_type=strbool)
timew_tf = _default("TIMEW_TF", default="f", arg_type=strbool)
pending_tasks_tf = _default("TASKW_PENDING_TF", default="f", arg_type=strbool)
timew_desc_override = _default("TIMEW_DESC_OVERRIDE", default="f", arg_type=strbool)

# Set timew_tf to true if the override is set.
if timew_desc_override:
    timew_tf = True

##############################
# TESTING TESTING TESTING

# taskw_tf = False
timew_tf = True
# timew_desc_override = True
# pending_tasks_tf = True
# notask_msg = "~No Task~"
##############################


def shorten(string, maxlen=maxlen):
    if len(string) <= maxlen:
        return string
    else:
        return string[: maxlen - 3] + "..."


def taskw_to_json(filter_string):
    return json.loads(
        subprocess.check_output("task " + filter_string + " export", shell=True)
    )


# Two functions: get_time_string, translate_time_string

# def timew_to_str(dom_string, decode=True):
#     try:
#         out = subprocess.check_output("timew get " + dom_string, shell=True)
#     except subprocess.CalledProcessError:
#         out = ""
#         decode = False
#     return out.decode("utf-8")[:-1] if decode else out


def get_time_bytes(dom_string):
    try:
        out = subprocess.check_output("timew get " + dom_string, shell=True)
    except subprocess.CalledProcessError:
        out = ""
    return out


def decode_time_bytes(in_bytes):
    to_string = in_bytes.decode("utf-8")[:-1]
    return to_string


def get_time_string(dom_string):
    in_string = get_time_bytes(dom_string)
    return decode_time_bytes(in_string)


def export_taskw():
    j = taskw_to_json("+ACTIVE")
    max_urg = 0
    if len(j) > 0:
        if urgency_tf:
            for i in range(len(j)):
                if j[i]["urgency"] > j[max_urg]["urgency"]:
                    max_urg = i
        return j[max_urg]["description"], len(j)
    else:
        return notask_msg, 0


def export_pending():
    return len(taskw_to_json("+PENDING"))


def export_timew_active():
    return b"1" in get_time_bytes("dom.active")


def export_timew_text():
    timew_txt = get_time_string("dom.active.tag.1")
    return timew_txt if export_timew_active() else notask_msg


def pad_time(s):
    return s if len(s) == 2 else "0" + s


def extract_time(s, t):
    match_list = re.findall(r"\d?\d" + s, t)
    return pad_time(match_list[0][:-1]) if len(match_list) > 0 else "00"


def translate_timew_string(timew_in_str):
    #    timew_in_str = timew_to_str("dom.active.duration")
    duration_hrs = extract_time("H", timew_in_str)
    duration_mins = extract_time("M", timew_in_str)
    return duration_hrs + ":" + duration_mins


def main():
    task_desc = ""
    task_append = ""
    timew_duration = ""
    pending_text = ""
    if taskw_tf:
        descr, task_num = export_taskw()
        task_desc = shorten(descr)
        if task_num > 1:
            task_append = " + " + str(task_num - 1)

    if timew_tf:
        get_string = get_time_string("dom.active.duration")
        timew_duration = (
            translate_timew_string(get_string) + " " if export_timew_active() else ""
        )

    if timew_desc_override or not taskw_tf:
        task_desc = shorten(export_timew_text())

    if pending_tasks_tf:
        pending_text = f" [{export_pending()}]"

    bar_text = timew_duration + task_desc + task_append + pending_text
    return bar_text


if __name__ == "__main__":
    print(main())
