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
git clone https://github.com/patryklaskowski/Measure_System_Resources.git && \
cd Measure_System_Resources
```

### 1a) Create and activate virtual environment (optional but recommended).
```
python3.7 -m venv env && \
source env/bin/activate
```

### 2) Install requirements
```
python3.7 -m pip install -r requirements.txt
```

### 2a) Test
```
python3.7 test.py
```

![Terminal screenshot](https://github.com/patryklaskowski/Measure_System_Resources/blob/main/images/terminal_01.png?raw=true)

On path there is new XLS `Measure_System_Resources/performance_1610449879.xlsx`

![XLS screenshot](https://github.com/patryklaskowski/Measure_System_Resources/blob/main/images/xls_01.png?raw=true)

### 3) Import the ```record_system_performance``` function
Great way is to add the path of */Measure_System_Resources* to sys.path. This step helps python interpreter to find the tool.

```python
import sys

tool_path = '/abolute/path/to/the/Measure_System_Resources'
sys.path.insert(0, tool_path)

from performance import record_system_performance

# The rest
# of your code
# ...
```

### 4) Run

```python
# The rest
# Of your code
# ...

import os
import time

# Your function to measure
def sleep_five_sec():
    time.sleep(5)

# Path where XLS file will be saved
filename = f'performance_{round(time.time())}.xlsx'
cur_abspath = os.path.abspath(os.path.curdir)
path = os.path.join(cur_abspath, filename)
    
# show time
record_system_performance(path, sleep_five_sec, timeout=20, sleep_around=5, stop=False)
```

---

# TODO:

- [ ] Show example plots
- [ ] Describe `record_system_performance(path, sleep_five_sec, timeout=20, sleep_around=5, stop=False)` attributes
- [ ] Thread should activate process with e.g. Event(). Now sleep_around is not symmetric.
