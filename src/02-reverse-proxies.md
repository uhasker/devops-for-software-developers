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

The `server` block defines the configuration for a specific (virtual) server.

The `listen 80` directive tells Nginx to listen on port 80 for incoming HTTP requests.

The `server_name` specifies the server names this server will respond to.
Currently we specified the wildcard `_` which means that this block will handle requests for any server name (that doesn't match another specific block).
We will replace this wildcard with an actual domain in the domain chapter.

The `location` block specifies how to process requests for a particular location.
Here, we tell Nginx to forward all requests to `127.0.0.1:8000` (where our `gunicorn` service is running) using the `proxy_pass` directive.
Additionally, we set HTTP headers to Nginx will include when forwarding requests to the backend server.

Now that we have created, the file let's enable the new config.

For this, you need to create a symlink from `sites-enabled` to `sites-available`:

```sh
sudo ln -s /etc/nginx/sites-available/example /etc/nginx/sites-enabled/example
```

You should also remove the `default` symlink from `sites-enabled`:

```sh
sudo trash-put /etc/nginx/sites-enabled/default
```

Reload Nginx to apply the changes:

```sh
sudo systemctl reload nginx
```

Note that there is a difference between `systemctl restart` and `systemctl reload`.
The first command completely stops the service and then starts it again.
The second command only reloads the configuration files and applies changes without stopping the service.

Now that we've started our reverse proxy, you can `curl` your service at port `80` aswell:

```sh
curl 127.0.0.1:80/hello
```
