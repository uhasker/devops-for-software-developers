# Domains

Setting up a domain is a relatively straightforward process.

First, you need to acquire a domain.

Second, you need to create an A record that points your domain to the public IP address of your server.

Let's say your acquired domain is `yourdomain.com` and the public IP of your server is `1.2.3.4`.
Then you would need to create an A record for example.com pointing to `1.2.3.4`.

Now you can curl `http://yourdomain.com/hello` instead of `http://1.2.3.4/hello`.

Additionally, you should set the `server_name` in Nginx config to `yourdomain.com`.
