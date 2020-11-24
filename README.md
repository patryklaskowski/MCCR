---
# Measure System Resources

Track and save system resources consumption while **YOUR** function is running.
- [x] per CPU (%),
- [x] Network sent/recv,
- [x] RAM,
- [x] Timestamp.

---
# Overview

- ```performance.py``` is main module that stores ```record_system_performance``` function which do the work.

---
# How to
### 1) Download the repository
```
git clone https://github.com/patryklaskowski/MCSR.git 
cd MCSR
```
#### 1a) Optionally create and run virtual environment
If you want to work from within the venv make sure all the necessary libraries your program needs are installed as well.
```
python3.7 -m venv env
source env/bin/activate
```
### 2) Install requirements for this tool
```
pip install -r requirements.txt
```
### 3) Import the ```record_system_performance``` function
Great way is to add the path of */Measure_System_Resources* to sys.path. This step helps python interpreter to find the tool.
```python
import sys

tool_path = '/abolute/path/to/the/Measure_System_Resources'
sys.path.insert(0, tool_path)

from performance import record_system_performance

# The rest
# of your fancy code
# ...
```
### 4) Run
```python
# The rest
# Of your fancy code
# ...

import os
import time

# Your function
def sleep_five_sec():
    time.sleep(5)

# Filename
filename = f'performance_{round(time.time())}.xlsx'
cur_abspath = os.path.abspath(os.path.curdir)
path = os.path.join(cur_abspath, filename)
    
# show time
record_system_performance(path, sleep_five_sec, timeout=20, sleep_around=5, stop=False)
```
