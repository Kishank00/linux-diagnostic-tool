def is_cpu_high(snapshot):
    cpu_usage = float(snapshot["cpu_usage_percent"])
    return cpu_usage >= 80

def is_memory_high(snapshot):
    memory_usage = float(snapshot["memory_usage_percent"])
    return memory_usage >= 80