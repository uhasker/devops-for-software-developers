# SSL Certificates

## Generate an SSL certificate

Let's generate a self-signed SSL certificate:

```sh
sudo openssl req -newkey rsa:2048 -nodes -keyout /tmp/localhost.key -x509 -days 365 -out /tmp/localhost.crt
```

Update nginx configuration for SSL at `/etc/nginx/sites-available/example`:

```
server {
    listen 80;
    server_name localhost;

    # Redirect HTTP traffic to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name localhost;

    # SSL certificate and key
    ssl_certificate /tmp/localhost.crt;
    ssl_certificate_key /tmp/localhost.key;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
