# Vimeo Log Stat Tracker

This is a single threaded python application that takes in a log file of any size and reads line by line until the end is reached. It will log messages as it encounters new domains, and some small logic and feedback stages to improve developer experience (DX) and user experience (UX). 

### Instructions
Ensure `get_stats.py` is executable by running on a *nix system 
```bash
chmod +x ./get_stats.py
```

You can optionally specify a start date and an end date via timestamp. For example, 

```bash
./get_stats.py --start 1493969101.647 --end 1493969101.666
```


### Example output


### Assumptions


### Dependencies 

Python 3.x with `argparse`, `logging`, `datetime` and `sys` python modules.