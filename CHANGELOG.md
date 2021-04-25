# Changelog for taskw blocklet

This changelog follows the conventions of [keep a changelog](https://keepachangelog.com/en/1.0.0/)
and [semantive versioning](https://semver.org/spec/v2.0.0.html).

## UNRELEASED

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
