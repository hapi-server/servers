This repository contains lists of HAPI servers.

* `abouts.json` is the master list.
* `all.txt` - List of production HAPI servers (legacy file)
* `all_.txt` - Additional information about servers. To use until we have developed a schema for such information. (legacy file)
* `dev.txt` - List of HAPI servers under development and not production ready

Nightly, a process generates the legacy `all.txt` and `all_.txt` files using the content of `about.json`. `about.json`

To add a server, create an object with at least `x_url` and `id`.

If the server has an `/about` endpoint, this information is inserted into the server object in `about.json` on a nightly basis. If the server does not have an `/about` endpoint, missing information can be added into the server object in `about.json`. If the server is upgraded to have an `/about` response, any existing information is overwritten.
    
If you have developed a HAPI server and it is ready for production, and you would like to make it automatically visible to existing software in the HAPI ecosystem, please make a pull request that adds your server URL to `dev.txt` at https://github.com/hapi-server/servers. After the pull request is accepted, it will be visible at https://hapi-server.org/servers-dev, and we will run tests to verify that existing HAPI software has no issues with the server. At that point, we will move the server URL out of dev.txt and into `abouts.json`, at which point it will be visible at https://hapi-server.org/servers and in (at minimum) all of the client software listed at https://github.com/hapi-server?q=client-*&type=all.
