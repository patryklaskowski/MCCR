# decorators.py

import time
import functools
import psutil
import datetime
import threading


def stopwatch(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('| %30s |: Start %s() ' % ('@stopwatch', func.__name__))
        start = time.perf_counter()
        value = func(*args, **kwargs)
        stop = time.perf_counter()
        print('| %30s |: Stop %s() been running %2.2f second(s).' % ('@stopwatch', func.__name__, stop-start))
        return value
    return wrapper


def performance_to_excel(excel, sleep_around=5):
    """Decorator @performance
    
    Keyword arguments:
    excel        -- Excel type object
    sleep_around -- How long the resources will be recording before and after the function run
    -------------------
    Example:
    1)
    > performance_to_excel(excel, sleep_around)(_run_function_as_parallel_process)(func, timeout)

    2)
    > @performance_to_excel(excel, sleep_around)
    > def _run_function_as_parallel_process(func, timeout):
    >    pass
    >
    > _run_function_as_parallel_process(func, timeout)
    """

    def decorator_performance(func):

        def recording_thread(event, excel):
            """Meant to run as a thread!
            
            Keyword arguments:
            event -- threading.Event(). To stop this thread
            excel -- Excel type object
            
            Thread that records system performance until event occour.
            """
            event.wait()
            print('| %30s |' % (''))
            print('| %30s |: Recording!' % ('thread'))
            psutil.net_io_counters.cache_clear()
            while event.is_set():
                net_before = psutil.net_io_counters()
                # CPU performance per each
                perc = psutil.cpu_percent(interval=1, percpu=True)
                # Timestamp
                date = datetime.datetime.now().strftime("%H:%M:%S")# %d/%m/%Y")
                print('| %30s |: *%s timestamp...' % ('thread', date))
                ram = psutil.virtual_memory()
                net_after = psutil.net_io_counters()
                perc.append(date)
                # Ram performance
                perc.append(ram.percent)
                perc.append(ram.used)
                perc.append(ram.active)
                # Network performance
                perc.append(net_after.bytes_sent)
                perc.append(net_after.bytes_recv)
                perc.append(net_after.bytes_sent-net_before.bytes_sent)
                perc.append(net_after.bytes_recv-net_before.bytes_recv)

                excel.append_row(perc)
                excel.save()
            print('| %30s |: Stop recording!' % ('thread'))
            print('| %30s |' % (''))

        
        @functools.wraps(func)
        def wrapper_performance(*args, **kwargs):
            '''Wraps function to measure system performance
            
            '''
            print('| %30s |: Start %s() ' % ('@performance', func.__name__))

            # 1) Excel columns
            n_cpu_logical = psutil.cpu_count(logical=True)
            print('| %30s |: There is %2.0f logical CPU(s) available.' % ('@performance', n_cpu_logical))
            ram_total = psutil.virtual_memory().total
            print('| %30s |: There is %2.3f GB RAM in total.' % ('@performance', ram_total * 10**(-9)))
            column_names = [f'CPU {idx+1}' for idx in range(n_cpu_logical)]
            column_names.append('Datetime')
            column_names.append('RAM_percent')
            column_names.append('RAM_used')
            column_names.append('RAM_active')
            column_names.append('Net_sent')
            column_names.append('Net_recv')
            column_names.append('Net_sent_persec')
            column_names.append('Net_recv_persec')

            excel.create_column_names(column_names)
            excel.save()

            print('| %30s |: Excel saved with new column names on path "%s".' % ('@performance', excel.path))

            # 2) Run thread
            event = threading.Event()
            event.set()
            t = threading.Thread(target=recording_thread, kwargs={'event':event, 'excel':excel})
            t.start()
            time.sleep(sleep_around)

            print('| %30s |' % (''))
            print('| %30s |: ------------- Function call ------' % ('@performance'))
            value = func(*args, **kwargs)
            print('| %30s |: ------------- Function done ------' % ('@performance'))
            print('| %30s |' % (''))

            time.sleep(sleep_around)
            event.clear()
            t.join()
            print('| %30s |: Stop %s()' % ('@performance', func.__name__))
            return value

        return wrapper_performance

    return decorator_performance

