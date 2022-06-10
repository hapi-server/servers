This repository contains lists of HAPI servers.

* `all.txt` - List of production HAPI servers
* `all_.txt` - Additional information about servers. To use until we have developed a schema for such information. (A proposed schema can be found in `json` directory.)
* `dev.txt` - List of HAPI servers under development and not production ready

If you have developed a HAPI server and it is ready for production and you would like to make it automatically visible to existing software in the HAPI ecosystem, please make a pull request that adds your server URL to `dev.txt` at https://github.com/hapi-server/servers. After the pull request is accepted, it will be visible at https://hapi-server.org/servers-dev and we will run tests to verify that existing HAPI software has no issues with the server. At that point, we will move the server URL out of dev.txt and into `all_.txt` at which point it will be visible at https://hapi-server.org/servers and in (at minimum) all of the client software listed at https://github.com/hapi-server?q=client-*&type=all.
