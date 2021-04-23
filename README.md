# Taskwarrior active task blocklet

This blocklet shows what task(s) you currently have active in TaskWarrior.
The blocklet will display the description of one of the active tasks
and an indication of how many other active tasks you have.

## Config options

 - `TASKW_TF` : whether to display information about tasks (from taskwarrior)
 - `TIMEW_TF` : whether to display information about time durations (from timewarrior)
 - `TIMEW_DESC_OVERRIDE` : whether to pull task description information from taskwarrior (false) or timewarrior (true). Will also set `TIMEW_TF` to true.
 - `TASKW_MAX_LENGTH` : the number of characters to truncate long task descriptions at
 - `TASKW_NOTASK_MSG` : the text to display if there are no active tasks
 - `TASKW_SORT_URGENCY` : a boolean to determine whether to display the most urgent active task (or the default behaviour which is to display the task which has been active longest).
 

## Timewarrior integration

Integration between taskwarrior and timewarrior is via a taskwarrior hook that starts/stops timewarrior when you 
start/stop a task in taskwarrior.
What this means is that if you have multiple tasks ongoing, the current timew duration is for 
the *most recently started* task (and the time for the task started earlier will be stopped when a newer task is started).
So having multiple ongoing tasks doesn't really play nice with timewarrior.
To make sure the task description matches the task to which the timew duration refers,
we could do one of two things: 
optionally sort tasks by most recent start time, or
get the task description from timew directly.
The former would require a lot messing about parsing times and dates, 
so we can explore the latter.
Timewarrior tags don't have any sort of hierarchy, so there's no analogue of a task duration's "description" attribute in taskwarrior.
The description is passed to timewarrior as the first tag by the `on-modify` hook.

All this is to explain why only the following modes of use are properly 
supported.

### Single task taskw/timew integration

Set `TASKW_TF` true and `TIMEW_TF` true.
Use the standard `on-modify` hook, only ever have *one* ongoing task.
Description information is reliably drawn from taskwarrior.

### Timew standalone usage

Set `TASKW_TF` false and `TIMEW_TF` true.
When using `timew`, make sure that the *first* tag is the one you want to appear 
in the bar.
