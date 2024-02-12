import psutil

def get_system_info():
    # Retrieve system information using psutil library
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    network = psutil.net_io_counters()
    processes = list(psutil.process_iter())

    # Sort the processes by CPU usage in descending order
    processes.sort(key=lambda x: x.cpu_percent(), reverse=True)

    return cpu_percent, memory.percent, network, processes