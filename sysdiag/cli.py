import sys
from .cpu import cpu_diagnostics, load_diagnostics, cpu_usage
from .memory import memory_diagnostics
from .process import top_memory_processes, process_diagnostics
from .disk import disk_diagnostics

def main():
    print("Linux System Diagnostic Tool")
    if len(sys.argv) > 1:
        if sys.argv[1] == "cpu":
            cpu_diagnostics()
        elif sys.argv[1] == "load":
            load_diagnostics()
        elif sys.argv[1] == "usage":
            cpu_usage()
        elif sys.argv[1] == "memory":
            memory_diagnostics()
        elif sys.argv[1] == "process":
            if len(sys.argv) == 2:
                top_processes = top_memory_processes()
                print(f"{'PID':<8} {'Name':<20} {'RSS (MiB)':>12}")
                for process in top_processes:
                    rss_mib = process["VmRSS"] / 1024
                    print(f"{process['PID']:<8} {process['Name']:<20} {rss_mib:>10.2f} MiB")
            elif len(sys.argv) == 3:
                try:
                    pid = int(sys.argv[2])
                    process_diagnostics(pid)
                except ValueError:
                    print("PID must be a number")
        elif sys.argv[1] == "disk":
            disk_diagnostics()
        

if __name__ == "__main__":
    main()
