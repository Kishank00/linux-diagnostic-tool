from fastapi import APIRouter

from sysdiag.disk import read_disk_usage, read_inode_usage, get_mount_points, get_mounted_filesystem_usage

router = APIRouter(prefix="/disk", tags=["disk"])

@router.get("/")
def disk_usage():
    disk_usage = read_disk_usage()
    return disk_usage

@router.get("/summary")
def get_disk_summary():
    disk_usage = read_disk_usage()
    inode_usage = read_inode_usage()

    total_disk = (disk_usage.total) / (1024 ** 3)
    used = (disk_usage.used) / (1024 ** 3)
    free = (disk_usage.free) / (1024 ** 3)
    usage_percent = (disk_usage.used / disk_usage.total) * 100

    return {
        "Total Disk": round(total_disk, 2),
        "Used Disk": round(used, 2),
        "Free Disk": round(free, 2),
        "Usage Percent": round(usage_percent, 2),
        "inode_percent": round(inode_usage["Inodes used percent"], 2)
    }

@router.get("/mount-usage")
def get_mount_usage():
    mounts_usage = get_mounted_filesystem_usage()
    return mounts_usage
