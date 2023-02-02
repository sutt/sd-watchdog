# TEMP FILES
# these only have data on the most recently-run or
# currently-running target
PID_FILE            = "./tmp/targetapp.pid"
TMP_STDOUT          = "./tmp/targetapp_stdout.log"
TMP_STDERR          = "./tmp/targetapp_stderr.log"


# LOG FILES
# these are persistent and contain all data from
# all runs of the target app
LOG_STDERR          = "./logs/targetapp_stderr.log"
LOG_STDOUT          = "./logs/targetapp_stdout.log"
MONITOR_LOG         = "./logs/monitor.log"
SPAWN_LOG           = "./logs/launch.log"


# APP COMMANDS AND TIMEOUTS
# these control what targetapp to spawn
APP_COMMAND         = "python mock_app.py"
APP_CWD             = "./tests/"
APP_URL             = "http://127.0.0.1:5000"

# These control how many fails / how long to wait
# before tirggering a restart of the target app
# when the repeated health checks fail
POLL_INTERVAL_SECS  = 10
MAX_FAIL_CHECKS     = 1
STARTUP_GRACE_SECS  = 2


# TESTING SETTINGS
noisy               = True
max_polls           = 5


# OVERIDES
# all these variable overrides are in user_config.py
from user_config import *