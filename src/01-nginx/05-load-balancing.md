# Load Balancing

Start multiple instances of the app:

```sh
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
python -m uvicorn app.main:app --host 127.0.0.1 --port 8002
```

Update the configuration at at `/etc/nginx/sites-available/example`:

```
upstream fastapi_backend {
    # Define your FastAPI app instances
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    listen 80;
    server_name _;

    location / {
        # Use the load-balancer defined above
        proxy_pass http://fastapi_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Restart the service:

```sh
sudo systemctl restart nginx
```

By default, nginx uses the round-robin algorithm, which simply distributes every request evenly among the available servers.
Nginx also supports:

- `least_conn` for "least connections" which sends requests to the server with the fewest active connections
- `ip_hash` ensures that request for the same client IP always go to the same backend server
