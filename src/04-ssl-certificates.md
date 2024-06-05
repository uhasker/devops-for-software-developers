# SSL Certificates

Next, you will need to provision an SSL certificate.

Install:

```sh
sudo apt update
sudo apt install python3-venv libaugeas0
```

Setup a `venv`:

```sh
sudo python3 -m venv /opt/certbot/
sudo /opt/certbot/bin/pip install --upgrade pip
```

Install:

```sh
sudo /opt/certbot/bin/pip install certbot certbot-nginx
sudo ln -s /opt/certbot/bin/certbot /usr/bin/certbot
```

Run:

```sh
sudo certbot --nginx
```

Enter the fields.

This will also make changes to your nginx config:

```
server {
    server_name yourdomain.com;

    location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/example.titanom.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/example.titanom.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}

server {
    listen 80;
    server_name yourdomain.com;

    if ($host = yourdomain.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    return 404; # managed by Certbot
}
```

Note the additional directives.

The `listen 443 ssl` directive tells Nginx to listen for HTTPS connections on port 443.
We also specify the paths to the various files relevant for the SSL certificate.

Additionally, there is an HTTP to HTTP redirection block.
The purpose of this block is basically to redirect HTTP requests to the corresponding HTTPS URL ensuring additional security.

Again, reload `nginx`.

You should now be able to `curl` the site:

```sh
curl https://yourdomain.com/hello
```

## Automatic Renewal

TODO
