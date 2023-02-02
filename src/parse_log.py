

def tail_of_log(log_file, n_lines):
    with open(log_file, "r") as f:
        lines = f.readlines()
        return "".join(lines[-n_lines:])

def find_lines_with(lines, search_str):    
    return "".join([line for line in lines if search_str in line])

def parse_time(line):
    return line.split(" | ")[0]

def parse_monitor_log():
    with open(MONITOR_LOG, "r") as f:
        lines = f.readlines()
        start_lines = find_lines_with(lines, "start_app()")
        stop_lines = find_lines_with(lines, "stop_app()")
    
    start_times = [parse_time(line) for line in start_lines]
    stop_times = [parse_time(line) for line in stop_lines]

    # which one is last?
    a,b = len(start_lines), (stop_times)

