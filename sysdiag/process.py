import os

def get_process_ids():
    entries = os.listdir("/proc")
    
    process_ids = []
    for entry in entries:
        if entry.isdigit():
            process_ids.append(int(entry))

    return process_ids

def read_process_info(pid):
    try:
        with open(f"/proc/{pid}/status", "r") as file:
            name = ""
            state = ""
            process_id = 0
            ppid = 0
            vm_size = 0
            vm_rss = 0
            threads = 0

            for line in file:
                values = line.split()

                if values[0] == "Name:":
                    name = values[1]
                elif values[0] == "State:":
                    state = values[1]
                elif values[0] == "Pid:":
                    process_id = int(values[1])
                elif values[0] == "PPid:":
                    ppid = int(values[1])
                elif values[0] == "VmSize:":
                    vm_size = int(values[1])
                elif values[0] == "VmRSS:":
                    vm_rss = int(values[1])
                elif values[0] == "Threads:":
                    threads = int(values[1])

        return {
            "Name": name,
            "State": state,
            "PID": process_id,
            "PPID": ppid,
            "VmSize": vm_size,
            "VmRSS": vm_rss,
            "Threads": threads
        }
    except FileNotFoundError:
        return None


# Restored from the backup so cli.py can import and display a single process.
def process_diagnostics(pid):
    process_info = read_process_info(pid)

    if process_info is None:
        print("Process Not Found")
    else:
        print(f"Name: {process_info['Name']}")
        print(f"State: {process_info['State']}")
        print(f"PID: {process_info['PID']}")
        print(f"PPID: {process_info['PPID']}")
        print(f"VmSize: {process_info['VmSize']} kB")
        print(f"VmRSS: {process_info['VmRSS']} kB")
        print(f"Threads: {process_info['Threads']}")


def get_all_process_info():
    process_ids = get_process_ids()
    processes = []

    for pid in process_ids:
        process_info = read_process_info(pid)

        if process_info is not None:
            processes.append(process_info)

    return processes


def top_memory_processes():
    processes = get_all_process_info()
    sorted_process = sorted(
        processes,
        key=lambda process: process["VmRSS"],
        reverse=True
    )
    return sorted_process[:5]
