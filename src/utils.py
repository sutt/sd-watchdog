import os
import time
from config import (
    PID_FILE, 
    TMP_STDOUT, 
    TMP_STDERR, 
    LOG_STDOUT,
    LOG_STDERR,
    MONITOR_LOG, 
    SPAWN_LOG,
)


def init_logs():
    
    # add nec. dirs if they don't exist
    if os.path.exists("./logs") is False:
        os.mkdir("./logs")
    
    if os.path.exists("./tmp") is False:
        os.mkdir("./tmp")
    
    # add log files if they don't exist
    for fn in [LOG_STDERR, LOG_STDOUT, MONITOR_LOG, SPAWN_LOG]:
        if not(os.path.exists(fn)):
            with open(fn, "w") as f:
                f.write("")
    
    return


def persist_and_reset_logs(pid=0):
    
    fn_pairs = [ (TMP_STDERR, LOG_STDERR), (TMP_STDOUT, LOG_STDOUT) ]

    for fnsrc, fndst in fn_pairs:
        
        # append tmp contents and associated pid to log
        with open(fnsrc, "r") as fsrc, open(fndst, "a") as fdst:
            fdst.write(f"===== pid={pid}\n")
            fdst.write(fsrc.read())
        
        # reset tmp files
        with open(fnsrc, "w") as f:
            f.write("")

    return


def log_data(
    log_type,
    event_name,
    data={},
):
    
    if   log_type   == "monitor_log": log_fn = MONITOR_LOG
    elif log_type   == "spawn_log"  : log_fn = SPAWN_LOG
    elif log_type   == "stdout_log" : log_fn = LOG_STDOUT
    elif log_type   == "stderr_log" : log_fn = LOG_STDERR
    else: raise Exception("Invalid log_type")
    
    s_data = "|".join(
        [f"{k}={v}" for k,v in data.items()]
    )
    
    with open(log_fn, "a") as f:
        f.write(f"{event_name} | {s_data}\n")

    return


def log_spawn():
    log_data(
        "spawn_log",
        "run_watch",
        {
            "now": time.time(),
        },
    )


def parse_top(top_output):
    """
    Parse the output of top and return a list of dictionaries
    """
    lines = top_output.splitlines()
    header = lines[0].split()
    processes = []
    for line in lines[1:]:
        process = {}
        for i, value in enumerate(line.split()):
            process[header[i]] = value
        processes.append(process)
    return processes

