import os
import time
import datetime
import subprocess
import requests

from .utils import (
    persist_and_reset_logs,
    log_data,
)

from config import (
    APP_COMMAND, 
    APP_CWD, 
    APP_URL,
    PID_FILE, 
    TMP_STDOUT, 
    TMP_STDERR, 
    MONITOR_LOG, 
    SPAWN_LOG,
    POLL_INTERVAL_SECS, 
    MAX_FAIL_CHECKS,
    STARTUP_GRACE_SECS,
    noisy, 
    max_polls,

)


SPAWN_START_TIME = None


def write_pid(pid):
    with open(PID_FILE, "w") as f:
        f.write(str(pid))


def read_pid():
    if os.path.exists(PID_FILE):
        with open(PID_FILE, "r") as f:
            return int(f.read())
    return None


def start_app():
    
    with open(TMP_STDOUT, "w") as out, \
         open(TMP_STDERR, "w") as err:

        process = subprocess.Popen(
                    APP_COMMAND.split(), 
                    stdout=out, 
                    stderr=err,
                    cwd=APP_CWD,
                    )
        
        pid = process.pid
        
        write_pid(pid)
        
        if noisy:print(f"Starting app pid={pid}")

        log_data(
            "monitor_log", 
            "start_app ",
            {
                "now": datetime.datetime.now(),
                "pid": pid,
            }
        )



def stop_app(deliberate=False):
    
    if noisy: print("Stopping app...")
    
    pid = read_pid()
    
    err_msg = ""
    try:
        # TODO - is 9 what we want to use to kill the script?
        os.kill(pid, 9)  
    # TODO - this could be just one Exception
    #        since we do the samething anyways
    except OSError:
        err_msg = f"Process {pid} not found"
        if noisy: print(err_msg)
    except Exception as e:
        err_msg = e
        if noisy: print(err_msg)
    
    os.remove(PID_FILE)

    log_data(
        "monitor_log", 
        "stop_app",
        {
            "now": datetime.datetime.now(),
            "deliberate": deliberate,
            "err_msg": err_msg,
        },
    )

    persist_and_reset_logs(pid=pid)
    

def ping_app(timeout=10):
    try:
        response = requests.get(APP_URL, timeout=timeout)
        return response.status_code == 200
    except:
        return False


def check_app(spawn_start_time=None):
    
    grace_checks = 0
    if spawn_start_time is not None:
        secs_since_spawn = time.time() - spawn_start_time
        grace_checks = max(0, STARTUP_GRACE_SECS - secs_since_spawn)
        grace_checks = int(grace_checks // POLL_INTERVAL_SECS)

    num_checks = max(MAX_FAIL_CHECKS, grace_checks)

    for num_check in range(num_checks):
        
        t0 = time.time()
        
        success = ping_app(timeout=POLL_INTERVAL_SECS - 1)
        
        if success: 
            return True
        
        log_data(
            "monitor_log", 
            " == ping_app failed",
            {
                "now": datetime.datetime.now(),
                "num_check": num_check,
            },
        )
        
        if noisy: print(" == ping_app failed")

        time.sleep(max(POLL_INTERVAL_SECS + t0 - time.time(), 0))

    return False


def run(spawn_start=None):
    
    pid = read_pid()
    
    if pid is None:
        start_app()
        return 
    
    b_healthy = check_app(spawn_start)
    
    if not(b_healthy):
        stop_app()
        start_app()

    return 


def watch_loop():

    if noisy: print("starting main_loop")
    
    poll_counter, spawn_start = 0, time.time()
    
    while True:        
        
        run(spawn_start)
        
        try:
            time.sleep(POLL_INTERVAL_SECS) 
            poll_counter += 1
            if noisy: print("Checking app...")
            
        # handle shutdown
        # TODO - handle SIGTERM etc
        except KeyboardInterrupt:
            if noisy: print("Stop app... keyboard interrupt")
            stop_app(deliberate=True)
            break
    
        # exit due to time limit
        if max_polls is not None and poll_counter >= max_polls:
            if noisy: print(f"Stop app... max polls={poll_counter}")
            stop_app(deliberate=True)
            break

    if noisy: print("main_loop exiting...")


if __name__ == "__main__":
    main_loop()