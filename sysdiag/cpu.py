import subprocess
import time

def cpu_diagnostics():
    print("Running CPU diagnostics...")
    logical_cpus = read_logical_cpu_count()
    print(f"Logical CPUs: {logical_cpus}")
    usage = cpu_usage()
    print(f"CPU Usage: {usage:.2f}%")
    load_info = load_diagnostics()
    print(f"Average load of 1 min: {load_info['load_1m']:.2f}")
    print(f"Average load of 5 min: {load_info['load_5m']:.2f}")
    print(f"Average load of 15 min: {load_info['load_15m']:.2f}")


def load_diagnostics():
    with open("/proc/loadavg", "r") as file:
        values = file.read().split()
        return {
            "load_1m": float(values[0]),
            "load_5m": float(values[1]),
            "load_15m": float(values[2])
        }


def read_cpu_stats():
    with open("/proc/stat", "r") as file:
        values = file.readline().split()
        user = int(values[1])
        nice = int(values[2])
        system = int(values[3])
        idle = int(values[4])
        iowait = int(values[5])
        irq = int(values[6])
        softirq = int(values[7])
        steal = int(values[8])
        guest = int(values[9])
        guest_nice = int(values[10])
        return {
            "user": user,
            "nice": nice,
            "system": system,
            "idle": idle,
            "iowait": iowait,
            "irq": irq,
            "softirq": softirq,
            "steal": steal,
            "guest": guest,
            "guest_nice": guest_nice
        }


def cpu_usage():
    sample1 = read_cpu_stats()

    time.sleep(2)

    sample2 = read_cpu_stats()

    total1 = (
        sample1["user"] + sample1["nice"] + sample1["system"] + sample1["idle"]
        + sample1["iowait"] + sample1["irq"] + sample1["softirq"] + sample1["steal"]
    )

    total2 = (
        sample2["user"] + sample2["nice"] + sample2["system"] + sample2["idle"]
        + sample2["iowait"] + sample2["irq"] + sample2["softirq"] + sample2["steal"]
    )

    iowait1 = sample1["iowait"]
    iowait2 = sample2["iowait"]

    idle1 = sample1["idle"]
    idle2 = sample2["idle"]

    total_delta = total2 - total1
    idle_delta = idle2 - idle1
    iowait_delta = iowait2 - iowait1

    busy_delta = total_delta - idle_delta - iowait_delta

    usage_percent = (busy_delta / total_delta) * 100

    return round(usage_percent, 2)

def read_logical_cpu_count():
    result = subprocess.run(
        ["nproc"],
        capture_output=True,
        text=True,
        check=True
    )
    return int(result.stdout.strip())