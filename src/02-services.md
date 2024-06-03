# Services

Create a service file at `/etc/systemd/system/example.service`:

```
[Unit]
Description=Example Flask app
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu
ExecStart=python -m gunicorn -w 4 --bind 0.0.0.0:8000 app:app

[Install]
WantedBy=multi-user.target
```

The description (pretty self-explanatory) provides a brief description of the service.

The "After" specifies service dependencies.
In this case, we want to make sure that the service starts after the network is up and running.

The "User" and "Group" specifies under which user and group the service will run.
The "WorkingDirectory" sets the working directory for the service - you will need to specify the directory containing the `app.py` file.

The "ExecStart" defines the command to start the service.

The "WantedBy=multi-user.target" is relatively complicated, but basically this is the standard system target for non-graphical multi-user systems (which most servers are).

Now you need to reload the systemd manager configuration:

```sh
sudo systemctl daemon-reload
```

Finally start the service:

```sh
sudo systemctl start example
```

You should also enable it to run on boot:

```sh
sudo systemctl enable example
```

Look at the status:

```sh
systemctl status example
```

You should see something like this:

```
● example.service - Example Flask App
     Loaded: loaded (/etc/systemd/system/example.service; enabled; preset: enabled)
     Active: active (running) since Mon 2024-06-03 11:18:28 UTC; 19s ago
   Main PID: 8743 (python)
      Tasks: 5 (limit: 4676)
     Memory: 68.2M (peak: 68.7M)
        CPU: 587ms
     CGroup: /system.slice/example.service
             ├─8743 python -m gunicorn -w 4 --bind 0.0.0.0:8000 app:app
             ├─8744 python -m gunicorn -w 4 --bind 0.0.0.0:8000 app:app
             ├─8745 python -m gunicorn -w 4 --bind 0.0.0.0:8000 app:app
             ├─8746 python -m gunicorn -w 4 --bind 0.0.0.0:8000 app:app
             └─8747 python -m gunicorn -w 4 --bind 0.0.0.0:8000 app:app

Jun 03 11:18:28 ip-172-31-31-82 systemd[1]: Started example.service - Example Flask App.
Jun 03 11:18:28 ip-172-31-31-82 python[8743]: [2024-06-03 11:18:28 +0000] [8743] [INFO] Starting gunicorn 22.0.0
Jun 03 11:18:28 ip-172-31-31-82 python[8743]: [2024-06-03 11:18:28 +0000] [8743] [INFO] Listening at: http://0.0.0.0:8000 (8743)
Jun 03 11:18:28 ip-172-31-31-82 python[8743]: [2024-06-03 11:18:28 +0000] [8743] [INFO] Using worker: sync
Jun 03 11:18:28 ip-172-31-31-82 python[8744]: [2024-06-03 11:18:28 +0000] [8744] [INFO] Booting worker with pid: 8744
Jun 03 11:18:28 ip-172-31-31-82 python[8745]: [2024-06-03 11:18:28 +0000] [8745] [INFO] Booting worker with pid: 8745
Jun 03 11:18:28 ip-172-31-31-82 python[8746]: [2024-06-03 11:18:28 +0000] [8746] [INFO] Booting worker with pid: 8746
Jun 03 11:18:28 ip-172-31-31-82 python[8747]: [2024-06-03 11:18:28 +0000] [8747] [INFO] Booting worker with pid: 8747
```
