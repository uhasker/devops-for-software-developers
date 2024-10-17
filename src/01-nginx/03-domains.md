# Domains

## Obtaining a domain

Modify your `/etc/hosts`:

```
127.0.0.1 example.com
```

In reality:

First, you need to acquire a domain.

Second, you need to create an A record that points your domain to the public IP address of your server.

Let's say your acquired domain is `yourdomain.com` and the public IP of your server is `1.2.3.4`.
Then you would need to create an A record for example.com pointing to `1.2.3.4`.

## Nginx Configuration

Update nginx configuration for domain at `/etc/nginx/sites-available/example`:

```
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Restart nginx.

## SSL Certificates for Domains

Let's generate a self-signed SSL certificate:

```sh
sudo openssl req -newkey rsa:2048 -nodes -keyout /tmp/example.com.key -x509 -days 365 -out /tmp/example.com.crt
```

Now you need to enter the FQDN as `example.com`.

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
    ssl_certificate /tmp/example.com.crt;
    ssl_certificate_key /tmp/example.com.key;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Restart nginx:

```sh
sudo systemctl restart nginx
```
