def is_cpu_high(snapshot):
    cpu_usage = float(snapshot["cpu_usage_percent"])
    return cpu_usage >= 80
