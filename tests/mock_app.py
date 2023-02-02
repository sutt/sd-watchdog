import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/error')
def always_error():
    raise Exception("Crash!")
    return "Crash"

@app.route('/kill')
def kill():
    os.kill(os.getpid(), 9)
    return "Killed"

if __name__ == '__main__':
    app.run(
        port=5000, 
        # debug=True,   # keep this off otherwise it will launch two processes
        # host="0.0.0.0"
        # use_reloader=False,
        )
