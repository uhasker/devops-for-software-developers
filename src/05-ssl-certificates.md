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
        server_name example.titanom.com;

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
    if ($host = example.titanom.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


        listen 80;
        server_name example.titanom.com;
    return 404; # managed by Certbot
}
```

Restart nginx.

Now you can curl yourdomain.com/hello.

## Automatic Renewal

TODO
