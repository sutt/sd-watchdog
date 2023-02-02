# sd-watchdog
<!-- inset image of robot dog -->
Devops to monitor and respawn your stable diffusion framework, and switch between frameworks without manual ssh access.

- **Process Driver** - switch between sd tools via http requests
- **Watchdog** - auto recover from crashes
- **Logger** - monitor and debug perfromance over time via http requests
<!-- add diagram -->


##### Use Case

This is suited for hobbyist programmer or artist who wants to run their stable diffusion framework on a cloud virtual machine. It takes into account the following challenges:

 - **Unstable -** Stable diffusion suites offered by Automatic1111, InvokeAI, and others have tremendous release momentum but remain unstable and frequently crash. 

 - **Exclusive -** Different strengths and features for each framework make the ability to switch worthwhile. It is difficult to have both frameworks running at the same time since they both load gigabytes of weights onto the GPU and take up lots of memory.

 - **Compute-Style VM -** These frameworks are only available to run on "compute" style cluster where we can attach high-end GPUs and state of the art CUDA versions. However these VM's aren't well suited for hosting robust web processes.
 
    
Without direct access to ssh access or ssh know-how this can making hosting your own stable diffusion deployment difficult. But, after setup, the sd-watchdog should automatically start the default stable diffusion process* on vm startup and enable you to monitor, switch and auto respawn crash processes

*: Most likely we will be launching either Automattic1111's `webui.sh` or InvokeAI's `invoke.py --web` which launch a gradio frontend 

----

### Quickstart

1. Clone down the repository to your cloud vm.
    ```bash
    $ git clone https://github.com/sutt/sd-watchdog
    ```

2. Edit `config.py` to point at a bash script which launches your stable diffusion engine.

    ```python
    APP_COMMAND = "webui.sh"  # to start an automattic111
    APP_CWD = "~/your/path/to/stable-diffusion-webui"
    # APP_COMMAND = "python scripts/invoke.py --web"  # to start an invokeai
    ```
    You can adjust these settings to temporary prefered in `user_config.py`. 
    <br>

3. Install dependencies and launch the sd-watchdog

    ```bash
    $ python -m venv venv/
    $ python watch.py --public-host
    
    >sd-watchdog running on port 5005...
    ```
    You can see all command line arguments [here](#Command-Line-Arguments)
    <br>

4. Enable http(s) firewall, locate public ip on vm
    By default, most compute vm's do not allow ingress of http(s) requests, only ssh requests.
    This can be done in gcloud console by clicking this button
    [alt](/gcloud-console-entable-https.png)


    This can also be done via `gcloud` command line:
    ```bash
    $ gcloud compute ls
    ```
    *note: if you don't have a public ip on your vm, you will need a way to access from the internet*
    *note: vm's without a certificate will not be able to accept https connections*

5. Check sd process, via command line or another server.
    Note you must run `watch.py` with `--public-host` argument for this to be reachable from an outside machine without port-forwarding and an ssh connection.
    From your local command line:
    ```bash
    $ curl http://<vm-ip>:5005/info
    {
        "is_running": true,
        "spawned_secs_ago": 560,
        "APP_CMD": "webui.sh",
        ...
    }
   ```
   From your browser, simply put `http://88.77.66.55:5005/info` into your browser, replacing the ip with the public ip of your vm.
   From another server, you can communicate via requests:
   ```python
    r = requests.get(url)
    print(r.json())
    >>> {
            "is_running": true,
            "spawned_secs_ago": 560,
            "APP_CMD": "webui.sh",
            ...
        }
   ```
   Beyond `/info`, see all available routes and RPC's [here](#a-list-of-routes-to-the-command-center)
   <br>

6. Register the watchdog to run on vm startup
    We've still been using ssh access to set all this up, but once we complete this step, the process
    This can vary depending on your vm's settings and os.
     - On Debian, you want to add a script which will activate the sd-watchdog's virtualenv and start the server, which by default will also start your

   within your `/var/run/` add the following file:
   ```

   ```


-----



#### Process Monitoring & Respawning
The watchdog's primary purpose is to restart the process of your choice when it crashes, and restore it with the desired settings.

The way the app checks if a process is running is to poll one of its processes with an http request, meaning we need an endpoint which will be run by the 

You can configure these in `config.py` to suit your needs:
```python

```



##### Command Line Arguments
 - `--no-server`do not run the server just launch the target app and run the watch_loop. The target app
 - `--no-watch`: do not run the watch_loop. This means the targetapp will not and cannot be launched. Useful if you just want to examine logs.
 - `--public-host`: expose the server to incoming http traffic.

##### Logging & Performance Monitoring
A history of :
 - your explicit command to start, stop, or switch sd tools logged to `spawn.log` 
 - detected crashes, attempted re-spawns  logged to `monitor.log`
 - stderr and stdout from the process messages in `targetapp_stderr.log`
 
Note that spawn, monitor and sterr can all be tied together by joining them on the pid of the launched process.

##### A list of routes to the command center
 - `/info`
 - `/read-current-[stderr/stdout]-log` - get the current . This will reset when the app is restarted



-----
### Development Notes

 - This project uses flask servers which, when run in debug mode (`app.run(..., debug=True)`), will launch two separate python processes which can be disruptive to the watchdog logic here. So those settings are turned off.
 - To test this app you can run `python src/test.py` which will run basic integration tests with `src/mock_app.py` instead of an actual sd framework. These are subject ot change:
    - both run a gradio frontend
 - Note on wsgi deployments - TODO