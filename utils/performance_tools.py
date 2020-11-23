# performance_tools.py

import psutil
import datetime
import os
from excel_module import Excel


def measure_func_performance(func, path):
    
    def measure_performance(event, excel):
        event.wait()
        print('(measure/record): Recording!')
        psutil.net_io_counters.cache_clear()
        while event.is_set():
            net_before = psutil.net_io_counters()
            perc = psutil.cpu_percent(interval=1, percpu=True)
            date = datetime.datetime.now().strftime("%H:%M:%S")# %d/%m/%Y")
            ram = psutil.virtual_memory()
            net_after = psutil.net_io_counters()
            
            perc.append(date)

            perc.append(ram.percent)
            perc.append(ram.used)
            perc.append(ram.active)

            perc.append(net_after.bytes_sent)
            perc.append(net_after.bytes_recv)
            perc.append(net_after.bytes_sent-net_before.bytes_sent)
            perc.append(net_after.bytes_recv-net_before.bytes_recv)

            excel.append_row(perc)
            print(f'(measure/record): *{date} appended row...')
            excel.save()
    

    def wrapper():
        ######################################################
        # Load excel
        assert '.xlsx' in path, 'Path must be excel file type (.xlsx)!'
        excel = Excel()
        if not os.path.isfile(path):
            excel.create(os.path.basename(path))

        excel.from_path(path)
        print(f'(measure/init): Excel opened from path "{excel.path}".')

        ######################################################
        # Set columns names in existing excel file
        #CPUS
        n_cpu_logical = psutil.cpu_count(logical=True)
        print(f'(measure/init): There is {n_cpu_logical} logical CPU(s) available.')
        #RAM
        ram_total = psutil.virtual_memory().total
        print(f'(measure/init): There is {ram_total} GB RAM in total.')

        column_names = [f'CPU {idx+1}' for idx in range(n_cpu_logical)]
        column_names.append('Datetime')
        column_names.append('RAM_percent')
        column_names.append('RAM_used')
        column_names.append('RAM_active')
        column_names.append('Net_sent')
        column_names.append('Net_recv')
        column_names.append('Net_sent_persec')
        column_names.append('Net_recv_persec')

        excel.create_columns_names(column_names)
        excel.save()
        print(f'(measure/init): Excel saved with column names on path "{excel.path}".')

        ######################################################
        # Run thread
        event = threading.Event()
        event.set()