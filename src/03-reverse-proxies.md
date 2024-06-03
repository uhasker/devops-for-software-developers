# Reverse Proxies

## Basic Idea

Typically you want to avoid clients communicating directly with your web server.

Instead you usually put a **reverse proxy** in front of it - a server that sits in front of your web server(s) and forwards client requests to those servers.

There a lot of benefits of reverse proxies.

First, you can use them for load balancing.
If you have a website that gets millions of users every day, you may not be able to handle all the traffic with a single server.
Here you could use the reverse proxy to distribute the incoming traffic between different web servers.

Second, you can use the reverse proxy for SSL encryption.
Encrypting and decrypting SSL/TLS is computationally expensive - a reverse proxy can free up resources for the origin server.

Third, a reverse proxy can cache content which improves performance.

Additionally, a reverse proxy improves security.

## A Simple Reverse Proxy with Nginx

You might need to install Nginx:

```sh
sudo apt install nginx
```

Let's setup a simple reverse proxy with Nginx.

Create a new configuration file in `/etc/nginx/sites-available/example`:

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

Enable the new config:

```sh
sudo ln -s /etc/nginx/sites-available/example /etc/nginx/sites-enabled/example
```

You should also remove the default site:

```sh
sudo trash-put /etc/nginx/sites-enabled/default
```

Restart Nginx to apply the changes:

```sh
sudo systemctl restart nginx
```

You can now query `localhost:80`.

You can also query:

```
curl 18.197.105.129:80/hello
```
