`abouts.json` is the HAPI project's master list of production HAPI servers.

`abouts-dev.json` is the HAPI project's master list of development HAPI servers.

`abouts-test.json` is the HAPI project's list of servers with data for testing clients.

If a server has an `/about` endpoint, this information is inserted into an object in the array in `abouts.json` on a daily basis.

If a server does not have an `/about` endpoint, or its `/about` response is incomplete, missing information will be added using content in `defaults/abouts.json` if it exists.

The code that does the daily updates is `abouts.py` in the [server-metadata](https://github.com/hapi-server/server-metadata/) repository.

If you have developed a HAPI server, and you would like to make it automatically visible to existing software in the HAPI ecosystem, please post an [issue with your server URL](https://github.com/hapi-server/servers/issues).

# Legacy Files

Nightly, a process generates the legacy `all.txt` and `all_.txt` files using the content of `abouts.json`.

* `all.txt` - List of production HAPI servers
* `all_.txt` - Additional information about servers
* `dev.txt` - List of HAPI servers under development and not production-ready
