from flask import Flask

from .monitor import (
    check_app,
)

from config import (
    TMP_STDERR,
    TMP_STDOUT,
    LOG_STDERR,
    LOG_STDOUT,
    SPAWN_LOG,
    MONITOR_LOG,
)

def create_routes(app):
    
    @app.route('/')
    @app.route('/info')
    def info():
        # TODO - add more info
        return 'watch.py on port 5005 ok'

    # @app.route('/switch')
    @app.route('/launch')
    def launch():
        return 'Not implemented yet'


    # @app.route('/reset')
    @app.route('/kill')
    def kill():
        return 'Not implemented yet'

    @app.route('/rm-pid-file')
    def rm_pid_file():
        return 'not implemented yet'
        # Send message explaining what this does
        # TODO - rm pid file

    @app.route('/app-status-check')
    def app_status():
        b_healthy = check_app()
        return f'app is responding to health check: {b_healthy}'


    @app.route('/read-current-err-log')
    def read_current_err_log():
        with open(TMP_STDERR, "r") as f:
            return f.read()


    @app.route('/read-current-out-log')
    def read_current_out_log():
        with open(TMP_STDOUT, "r") as f:
            return f.read()


    @app.route('/read-persist-err-log')
    def read_persist_err_log():
        with open(LOG_STDERR, "r") as f:
            return f.read()


    @app.route('/read-persist-out-log')
    def read_persist_out_log():
        with open(LOG_STDOUT, "r") as f:
            return f.read()


    @app.route('/read-monitor-log')
    def read_monitor_log():
        with open(MONITOR_LOG, "r") as f:
            return f.read()


    @app.route('/read-spawn-log')
    def read_spawn_log():
        with open(SPAWN_LOG, "r") as f:
            return f.read()


    @app.route('/watch-summary')
    def watch_summary():
        return 'not implemented yet'
        # TODO - last health check good, last bad
        # TODO - last spawn, last kill
        # TODO - last kill
