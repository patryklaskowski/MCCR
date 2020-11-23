# performance.py

from utils.excel_module import Excel
import os
import multiprocessing
import time
from utils.decorators import stopwatch, performance_to_excel
import datetime
import psutil


def nothing():
    pass

@stopwatch
def _run_function_as_parallel_process(func, timeout=10, stop=False):
    """Runs function as a parallel process
    
    Keyword arguments:
    func    -- function to run
    timeout -- max time after which process will be terminated (default 5)
    stop    -- determines if function stops when process finish (default False)
    """
    assert func, 'No function provided'
    assert timeout in range(1, 60+1), 'Function runtime must be in range 1 to 60 seconds.'
    multiprocessing.set_start_method('spawn')
    proc = multiprocessing.Process(target=func)
    # print('| %30s |: Process start.' % ('_parallel_process'))
    proc.start()

    for sec in range(timeout, 0, -1):
        if not proc.is_alive() and stop:
            break
        print('| %30s |: Subprocess timeout: %2.0f second(s) left.' % ('_parallel_process', sec))
        time.sleep(1)
    
    while proc.is_alive():
        proc.terminate()
    # print('| %30s |: Process done.' % ('_parallel_process'))


@stopwatch
def record_system_performance(path, func=nothing, timeout=20, sleep_around=5):

    print('| %30s |: Provided path: "%s"' % ('record_system_performance', path))
    
    ########################
    assert os.path.exists(os.path.dirname(path)), f'Directory "{os.path.dirname(path)}" not found.'
    assert os.path.splitext(path)[1] == '.xlsx', f'This is not valid excel file "{os.path.basename(path)}".'

    excel = Excel()
    if not os.path.isfile(path):
        excel.create_empty_workbook(path)
    excel.from_path(path)
    print('| %30s |: Excel object ready to run.' % ('record_system_performance'))
    ########################
    ###
    performance_to_excel(excel, sleep_around)(_run_function_as_parallel_process)(func, timeout)
    ##
    ########################
    # print('| %30s |: All done.' % ('record_system_performance'))