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

The server block defines the configuration for handling requests for a particular server or virtual host. Here, it configures Nginx to act as a reverse proxy for incoming HTTP traffic.

The directive `listen 80;` tells Nginx to listen for traffic on port 80, which is the default port for HTTP communication. This means that any HTTP requests sent to the server will be received and processed on this port, enabling Nginx to manage all such traffic.

The `server_name _;` directive is used to specify which domain names or IP addresses this server block should respond to. The underscore (\_) is a wildcard, meaning that this configuration will handle requests directed to any domain or IP address, unless another server block with a more specific domain configuration is defined elsewhere in the Nginx setup.

The `location /` block defines how to handle requests that match a particular path. In this case, the / path indicates that all requests sent to the server (regardless of specific subpaths) will be processed here. For instance, a request to /api or /login will both be matched by this configuration.

Within the location block, the `proxy_pass http://127.0.0.1:8000;` directive is crucial. It tells Nginx to forward incoming requests to a backend server running on the same machine (localhost) at port 8000. This effectively makes Nginx a reverse proxy, receiving requests from clients, passing them to the backend service, and then forwarding the backend’s response back to the client.

The `proxy_set_header` directives in this configuration customize the HTTP headers that Nginx sends along with the forwarded request to the backend server. These headers ensure that important information from the original client request is preserved and passed to the backend.

The `proxy_set_header Host $host;` line sets the Host header in the forwarded request to the value of $host, which represents the original Host header from the client. This is important because many backend servers use the Host header to determine which virtual host or application should handle the request, especially in cases where multiple services might be hosted.

The `proxy_set_header X-Real-IP $remote_addr;` directive adds the client’s real IP address to the X-Real-IP header. Since Nginx is positioned between the client and the backend server, the backend would otherwise see Nginx's IP address instead of the original client’s IP. This header ensures that the backend server knows the true IP of the client making the request.

The `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;` directive is used to create or append to the X-Forwarded-For header. This header keeps track of the original client’s IP address and any intermediary proxies that the request passed through. It is particularly useful for identifying the real client’s IP in cases where multiple proxy servers might be involved.

The `proxy_set_header X-Forwarded-Proto $scheme;` directive sets the X-Forwarded-Proto header to the protocol used in the original request, which could be either http or https. This allows the backend server to know whether the client’s original request was made over a secure or insecure connection. This information can be important when generating redirects or handling security-sensitive logic.

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
