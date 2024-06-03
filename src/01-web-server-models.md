# Web Server Models

## An Example

You might need to do this:

```sh
sudo apt update && sudo apt upgrade
sudo apt install python3-pip
python -m pip install flask gunicorn
```

Consider the following simple web server `app.py` written in Flask:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello, world!"
```

## CPU-Bound vs I/O-Bound Tasks

Consider the following simple web server `app.py` written in Flask:

```python
from flask import Flask, jsonify
import time

app = Flask(__name__)

def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

@app.route('/cpu_task', methods=['GET'])
def cpu_task():
    result = fibonacci(36)
    return f"Fibonacci(36) = {result}"

@app.route('/io', methods=['GET'])
def io_task():
    time.sleep(3)
    return jsonify({"message": "I/O task completed"})
```

We can run it like this:

```sh
python -m flask run
```

If you look at the console, you will see:

```
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
```

## Sync Workers

Let's use gunicorn:

```sh
python -m gunicorn -k sync -w 4 -b 0.0.0.0:8000 app:app
```

Gunicorn is based on something called the pre-fork worker model.

Let's have a look at the processes:

```sh
ps -aux | grep gunicorn
```

This is the output:

```
uhasker    27603  0.8  0.1  34736 21860 pts/1    S+   09:59   0:00 python -m gunicorn -w 4 -b 0.0.0.0:8000 app:app
uhasker    27661  0.6  0.1  43456 27096 pts/1    S+   09:59   0:00 python -m gunicorn -w 4 -b 0.0.0.0:8000 app:app
uhasker    27662  0.6  0.1  43456 27096 pts/1    S+   09:59   0:00 python -m gunicorn -w 4 -b 0.0.0.0:8000 app:app
uhasker    27663  0.6  0.1  43456 27096 pts/1    S+   09:59   0:00 python -m gunicorn -w 4 -b 0.0.0.0:8000 app:app
uhasker    27664  0.5  0.1  43456 27096 pts/1    S+   09:59   0:00 python -m gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

We can look at the relationships between the processes:

```sh
pstree -p 27603
```

This is the output:

```
python(27603)─┬─python(27661)
              ├─python(27662)
              ├─python(27663)
              └─python(27664)
```

Script:

```sh
#!/bin/bash

# Function to perform a curl request and print start and end times
perform_request() {
    local start_time=$(date +"%Y-%m-%d %H:%M:%S")
    echo "Start time: $start_time"

    curl -w "\n" -s http://127.0.0.1:8000/hello

    local end_time=$(date +"%Y-%m-%d %H:%M:%S")
    echo "End time: $end_time"
}

# Loop to perform 10 concurrent curl requests
for i in {1..10}; do
    perform_request &
done

# Wait for all background jobs to finish
wait
```

Output:

```
Start time: 2024-06-03 10:42:26
Start time: 2024-06-03 10:42:26
Start time: 2024-06-03 10:42:26
Start time: 2024-06-03 10:42:26
Start time: 2024-06-03 10:42:26
Start time: 2024-06-03 10:42:26
Start time: 2024-06-03 10:42:26
Start time: 2024-06-03 10:42:26
Start time: 2024-06-03 10:42:26
Start time: 2024-06-03 10:42:26
Fibonacci(36) = 14930352
End time: 2024-06-03 10:42:29
Fibonacci(36) = 14930352
End time: 2024-06-03 10:42:29
Fibonacci(36) = 14930352
End time: 2024-06-03 10:42:29
Fibonacci(36) = 14930352
End time: 2024-06-03 10:42:29
Fibonacci(36) = 14930352
End time: 2024-06-03 10:42:33
Fibonacci(36) = 14930352
End time: 2024-06-03 10:42:33
Fibonacci(36) = 14930352
End time: 2024-06-03 10:42:33
Fibonacci(36) = 14930352
End time: 2024-06-03 10:42:33
Fibonacci(36) = 14930352
End time: 2024-06-03 10:42:36
Fibonacci(36) = 14930352
End time: 2024-06-03 10:42:36
```

## Async Workers

Let's run async:

```
Start time: 2024-06-03 10:55:14
Start time: 2024-06-03 10:55:14
Start time: 2024-06-03 10:55:14
Start time: 2024-06-03 10:55:14
Start time: 2024-06-03 10:55:14
Start time: 2024-06-03 10:55:14
Start time: 2024-06-03 10:55:14
Start time: 2024-06-03 10:55:14
Start time: 2024-06-03 10:55:14
Start time: 2024-06-03 10:55:14
{"message":"I/O task completed"}
{"message":"I/O task completed"}
{"message":"I/O task completed"}
{"message":"I/O task completed"}
End time: 2024-06-03 10:55:17
End time: 2024-06-03 10:55:17
End time: 2024-06-03 10:55:17
End time: 2024-06-03 10:55:17
{"message":"I/O task completed"}
{"message":"I/O task completed"}
{"message":"I/O task completed"}
{"message":"I/O task completed"}
End time: 2024-06-03 10:55:20
End time: 2024-06-03 10:55:20
End time: 2024-06-03 10:55:20
End time: 2024-06-03 10:55:20
{"message":"I/O task completed"}
{"message":"I/O task completed"}
End time: 2024-06-03 10:55:23
End time: 2024-06-03 10:55:23
```

This is no longer great - most of the time our CPU will spend idling around.

Let's install eventlet:

```sh
python -m pip install gunicorn[eventlet]
```

Now let's run the application using the `eventlet` worker:

```sh
python -m gunicorn -w 4 -k eventlet -b 0.0.0.0:8000 app:app
```

Again run `load.sh`:

```
Start time: 2024-06-03 11:00:04
Start time: 2024-06-03 11:00:04
Start time: 2024-06-03 11:00:04
Start time: 2024-06-03 11:00:04
Start time: 2024-06-03 11:00:04
Start time: 2024-06-03 11:00:04
Start time: 2024-06-03 11:00:04
Start time: 2024-06-03 11:00:04
Start time: 2024-06-03 11:00:04
Start time: 2024-06-03 11:00:04
{"message":"I/O task completed"}
{"message":"I/O task completed"}
{"message":"I/O task completed"}
{"message":"I/O task completed"}
{"message":"I/O task completed"}
{"message":"I/O task completed"}
{"message":"I/O task completed"}
{"message":"I/O task completed"}
{"message":"I/O task completed"}
{"message":"I/O task completed"}
End time: 2024-06-03 11:00:07
End time: 2024-06-03 11:00:07
End time: 2024-06-03 11:00:07
End time: 2024-06-03 11:00:07
End time: 2024-06-03 11:00:07
End time: 2024-06-03 11:00:07
End time: 2024-06-03 11:00:07
End time: 2024-06-03 11:00:07
End time: 2024-06-03 11:00:07
End time: 2024-06-03 11:00:07
```

## FastAPI

TODO
