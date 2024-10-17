# Reverse Proxy

## Install

Installation:

```sh
sudo apt install nginx
```

Enable the nginx service:

```sh
sudo systemctl start nginx
sudo systemctl status nginx
```

## Configuration

Let's configure a reverse proxy that forwards HTTP request from port 80 to our FastAPI application on port 8000.
A reverse proxy is a server that sits in front of web servers and forwards client request to these web servers.

Benefits of a reverse proxy (generally decoupling application code from infrastructure):

- load balancing
- protection from DDoS attacks
- caching
- SSL encryption

Add the following configuration at `/etc/nginx/sites-available/example`:

```
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the nginx configuration:

```sh
sudo ln -s /etc/nginx/sites-available/example /etc/nginx/sites-enabled/example
```

Test the configuration:

```sh
sudo nginx -t
```

Start the Python service in `examples/app-example`:

```sh
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Restart the service:

```sh
sudo systemctl restart nginx
```

You should now be able to `curl` the service both through `127.0.0.1:80` and `127.0.0.1:8000`.
