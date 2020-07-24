# Vimeo Log Stat Tracker

This is a single threaded python application that takes in a log file of any size and reads line by line until the end is reached. It will log messages as it encounters new domains, and some small logic and feedback stages to improve developer experience (DX) and user experience (UX). 

Please note, this is a contrived example of how to make a tool to do this. It is not complete, and there exists already built industry wide solutions that are better than this script such as an ELK stack.

### Instructions
Ensure `get_stats.py` is executable by running on a *nix system 
```bash
chmod +x ./get_stats.py
```

You can optionally specify a start date and an end date via timestamp. For example, 

```bash
./get_stats.py --start 1493969101.647 --end 1493969101.666
```

By default, if you do not specify astart or end date, the default values are 1 hour ago for the start up until the present for the end.


### Example output
![output](./result.gif)

### Assumptions

- Timestamps were in the default python timestamp format (format provided by datetime.timestamp() function)

- Single threading/performance on a 10Gb+ size file is irrelevant

### Improvements

- CI/CD pipeline with unit/integration testing
- Git Hooks to do linting/formatting pre-commit
- Git repo with relevant Jira/Slack/etc integrations.

### Dependencies 

Python 3.x with `argparse`, `logging`, `datetime` and `sys` python modules.