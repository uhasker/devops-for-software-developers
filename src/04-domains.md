# Domains

Let's say your IP address is 18.197.105.129.

First, you need to buy a domain.

Second, you need to create an A record that points to that IP address.

Let's say your domain is `yourdomain.com`.
Then you would need to create an A record for example.com pointing to 18.197.105.129.

Now you can curl `http://yourdomain.com/hello`

Let's also change `server_name` to `yourdomain.com`.
