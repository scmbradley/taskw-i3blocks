# Changelog for taskw blocklet

This changelog follows the conventions of [keep a changelog](https://keepachangelog.com/en/1.0.0/)
and [semantic versioning](https://semver.org/spec/v2.0.0.html).

## v0.3.0

### ADDED

 - `TASKW_MAIN_FILTER` option now allows you to select a filter other than `+ACTIVE` to display

### OTHER

 - Made a minor change to `bumpversion` config so that the changelog 
 updates to the appropriate tag.
 A side effect of this is that I cannot bump version without having
 something listed in the "unreleased" section.


## v0.2.4

### OTHER

 - Changed the bumpversion commit message
 - Added version information to `test_basic.py` and `i3blocks.conf`
 - Added unit tests for more functions

## v0.2.3

### OTHER

 - Wrote some tests
 - Did some refactoring of the taskw script

## v0.2.2

### OTHER

 - Moved to using `bumpversion` to update versions. Nothing to see here.

## v0.2.1

### OTHER

 - Updated readme regarding python versions and dependencies
 - Removed a helper script from the git repo
 - Added some information to the top of the changelog

## v0.2.0

### ADDED

 - Config options to turn on/off calling taskwarrior
 - Config options to turn on/off calling timewarrior
 - Timewarrior task description override
 - Timewarrior display elapsed time option
 - Taskwarrior total pending tasks option
 
### FIXED

 - Refactored the code that extracts information from shell commands
 so that is it now less of a mess

## v0.1.0

### ADDED

 - Basic functioning of taskw block
 - Option for truncating text
 - Option for no task message
 - Option to sort by urgency
