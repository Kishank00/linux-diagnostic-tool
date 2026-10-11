import shutil
import os
import time

def read_disk_usage(path="/"):
    return shutil.disk_usage(path)


def disk_diagnostics():
    usage = read_disk_usage()
    inode_info = read_inode_usage()
    total_disk = (usage.total) / (1024 ** 3)
    used = (usage.used) / (1024 ** 3)
    free = (usage.free) / (1024 ** 3)
    usage_percent = (usage.used / usage.total) * 100
    print(f"Total_Disk: {total_disk:.2f} GiB")
    print(f"Used Disk: {used:.2f} GiB")
    print(f"Free Disk: {free:.2f} GiB")
    print(f"Disk Usage Percentage: {usage_percent:.2f}%")
    print(f"Inode Usage: {inode_info['Inodes used percent']:.2f}%")
    print(f"Total Inodes: {inode_info['Total inodes']}")
    print(f"Used Inodes: {inode_info['Used inodes']}")
    print(f"Free Inodes: {inode_info['Free inodes']}")
    print(f"Available Inodes: {inode_info['Available inodes']}")

    if usage_percent >= 90:
        print("Disk Usage is in Critical State, please expand the disk size")
    elif usage_percent >=80:
        print("Disk Usage is in Warning State, please look into the disk")
    else:
        print("Disk is OK")
    mounted_filesystem_diagnostics()
    print("Disk I/O Diagnostics")
    io_info = disk_io_diagnostics()
    if io_info is None:
        print("Disk I/O metrics unavailable.")
    else:
        print(f"Read IOPS: {io_info['Read_IOPS']:.2f}")
        print(f"Write IOPS: {io_info['Write_IOPS']:.2f}")
        print(f"Read Throughput: {io_info['Read_Data_per_Sec']:.2f} MiB/s")
        print(f"Write Throughput: {io_info['Write_Data_per_Sec']:.2f} MiB/s")

    inode_percent = inode_info["Inodes used percent"]
    if inode_percent >= 90:
        print("Critical")
    elif inode_percent >= 80:
        print("Warning")
    else:
        print("OK")

def read_inode_usage(path="/"):
    stats = os.statvfs(path)
    used_inodes = stats.f_files - stats.f_ffree
    inode_usage_percent = (used_inodes / stats.f_files) * 100
    return {
        "Total inodes": stats.f_files,
        "Free inodes": stats.f_ffree,
        "Available inodes": stats.f_favail,
        "Used inodes": used_inodes,
        "Inodes used percent": round(inode_usage_percent, 2)
    }

def get_mount_points():
    mounts = []
    with open("/proc/mounts", "r") as file:
        for mount in file:
            values = mount.split()

            mounts.append({
                "source": values[0],
                "mount_point": values[1],
                "filesystem_type": values[2]
            })

    return mounts

def mounted_filesystem_diagnostics():
    mounts = get_mount_points()
    
    for mount in mounts:
        mount_point = mount["mount_point"]
        if mount["filesystem_type"] not in ["ext4", "xfs", "vfat"]:
            continue

        try:
            usage = read_disk_usage(mount_point)
        except PermissionError:
            print(f"Skipping inaccessible mount: {mount_point}")
            continue

        print(
            f"{mount_point:<15} "
            f"{usage.total / (1024 ** 3):>10.2f} GiB "
            f"{usage.used / (1024 ** 3):>10.2f} GiB "
            f"{usage.free / (1024 ** 3):>10.2f} GiB"
        )

def get_mounted_filesystem_usage():
    mounts = get_mount_points()
    filesystem_usage = []

    for mount in mounts:
        if mount["filesystem_type"] not in ["ext4", "xfs", "vfat"]:
            continue

        mount_point = mount["mount_point"]

        try:
            usage = read_disk_usage(mount_point)
        except (PermissionError, OSError):
            continue

        total_gib = usage.total / (1024 ** 3)
        used_gib = usage.used / (1024 ** 3)
        free_gib = usage.free / (1024 ** 3)

        usage_percent = (
            (usage.used / usage.total) * 100
            if usage.total > 0
            else 0
        )

        filesystem_usage.append({
            "source": mount["source"],
            "mount_point": mount_point,
            "filesystem_type": mount["filesystem_type"],
            "total_gib": round(total_gib, 2),
            "used_gib": round(used_gib, 2),
            "free_gib": round(free_gib, 2),
            "usage_percent": round(usage_percent, 2)
        })

    return filesystem_usage

def read_disk_io_stats(device_name="nvme0n1"):
    with open("/proc/diskstats", "r") as file:
        for line in file:
            values = line.split()
            if values[2] == device_name:
                reads_completed = int(values[3])
                sectors_read = int(values[5])
                writes_completed = int(values[7])
                sectors_written = int(values[9])
                return {
                    "Reads Completed": reads_completed,"Sectors Read": sectors_read,
                    "Writes Completed": writes_completed,"Sectors Written": sectors_written
                    }

def disk_io_diagnostics(device_name="nvme0n1"):
    start_time = time.monotonic()
    sample1 = read_disk_io_stats(device_name)
    if sample1 is None:
        print("The requested device wasn't found in /proc/diskstats")
        return None

    time.sleep(1)

    sample2 = read_disk_io_stats(device_name)
    if sample2 is None:
        print("The requested device wasn't found in /proc/diskstats")
        return None
    
    elapsed_seconds = time.monotonic() - start_time
    print(f"Elapsed time: {elapsed_seconds:.2f} seconds")

    reads_delta = sample2["Reads Completed"] - sample1["Reads Completed"]
    sectors_read_delta = sample2["Sectors Read"] - sample1["Sectors Read"]

    writes_delta = sample2["Writes Completed"] - sample1["Writes Completed"]
    sectors_written_delta = sample2["Sectors Written"] - sample1["Sectors Written"]

    read_iops = reads_delta / elapsed_seconds
    write_iops = writes_delta / elapsed_seconds

    read_mib_per_sec = (sectors_read_delta * 512) / elapsed_seconds / (1024 ** 2)
    write_mib_per_sec = (sectors_written_delta * 512) / elapsed_seconds / (1024 ** 2)

    return {
        "Read_Delta": reads_delta,
        "Sectors_Read_Delta": sectors_read_delta,"Writes_Delta": writes_delta,
        "Sectors_Written_Delta": sectors_written_delta,
        "Read_IOPS": read_iops,
        "Write_IOPS": write_iops,
        "Read_Data_per_Sec": read_mib_per_sec,
        "Write_Data_per_Sec": write_mib_per_sec
        }