import psutil

async def get_disk_space():
    '''
    Get disk space information for sending to clients
    '''
    disk = psutil.disk_usage('/')
    return {
        "free": disk.free,
        "total": disk.total,
        "percent": disk.percent
    }