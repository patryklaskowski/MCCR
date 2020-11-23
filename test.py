# test.py

from performance import record_system_performance
import os
import time

# Arbitralna funkcja do testu
def sleep_five_sec():
    print('(my_func): Start')
    for _ in range(5, 0, -1):
        time.sleep(1)
    print('(my_func): Stop')
    return 'ok'

 
if __name__ == '__main__':
    # Initialize
    filename = f'performance_{round(time.time())}.xlsx'
    cur_abspath = os.path.abspath(os.path.curdir)
    path = os.path.join(cur_abspath, filename)
    
    # show time
    print(40*'-')
    record_system_performance(path, sleep_five_sec, timeout=10, sleep_around=4)
    print(40*'-')