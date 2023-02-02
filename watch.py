import sys
import time
import argparse
from threading import Thread
from flask import Flask
from src.utils import init_logs, log_spawn
from src.routes import create_routes
from src.monitor import watch_loop
    

def run(
    run_watchloop=True,
    run_server=True,
    host="127.0.0.1",
    port=5005,
):

    init_logs()
    
    log_spawn()
    
    if run_watchloop:
        # run watch_loop in separate thread to avoid blocking 
        # the launch of the webapp below
        # move this above the kill route to interact with it?
        t = Thread(target=watch_loop)
        t.start()

    if run_server:    

        app = Flask(__name__)

        create_routes(app)

        app.run(
            port=5005, 
            host=host
        )
        # does thread stay running if --no-server called?

    

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-server', action='store_true')
    parser.add_argument('--no-watch', action='store_true')
    parser.add_argument('--public-host', action='store_true')
    parser.add_argument('--port', type=int, default=5005)
    
    args = vars(parser.parse_args())
        
    run(
        run_watchloop   =not(args['no_watch']),
        run_server      =not(args['no_server']),
        host            ="0.0.0.0" if args['public_host'] \
                        else "127.0.0.1",
        port            =args['port'],
    )

