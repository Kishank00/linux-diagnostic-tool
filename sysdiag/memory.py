def read_memory_info():
    mem_total = 0
    mem_available = 0
    swap_total = 0
    with open("/proc/meminfo", "r") as file:
        for line in file:
            values = line.split()

            if values[0] == "MemTotal:":
                mem_total = int(values[1])

            elif values[0] == "MemAvailable:":
                mem_available = int(values[1])

            elif values[0] == "SwapTotal:":
                swap_total = int(values[1])

    return {
        "mem_total": mem_total,
        "mem_available": mem_available,
        "swap_total": swap_total
        }

def memory_diagnostics():
    memory_info = read_memory_info()

    total_gib = memory_info["mem_total"] / (1024 * 1024)
    print(f"Total Memory: {total_gib:.2f}GiB")

    available_gib = memory_info["mem_available"] / (1024 * 1024)
    print(f"Memory Available: {available_gib:.2f}GiB")

    used_memory = (memory_info["mem_total"] - memory_info["mem_available"]) / (1024 * 1024)
    print(f"Used Memory: {used_memory:.2f}GiB")

    used_memory_kb = (memory_info["mem_total"] - memory_info["mem_available"])
    memory_percent = (used_memory_kb / memory_info["mem_total"]) * 100
    print(f"Memory Usage: {memory_percent:.2f}%")

    swap_total = memory_info["swap_total"]
    if swap_total == 0:
        print("Swap Disabled")
    else:
        swap_gib = swap_total / (1024 * 1024)
        print(f"Swap Total: {swap_gib:.2f} GiB")