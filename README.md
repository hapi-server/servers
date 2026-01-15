`abouts.json` is the HAPI project's master list of production HAPI servers.

`abouts-dev.json` is the HAPI project's master list of development HAPI servers.

`abouts-test.json` is the HAPI project's list of servers with data for testing clients.

`abouts-all.json` ?

If the server has an `/about` endpoint, this information is inserted into the server object in `about.json` on a nightly basis. If the server does not have an `/about` endpoint, missing information can be added into the server object in `about.json`. If the server is upgraded to have an `/about` response, any existing information is overwritten.

If you have developed a HAPI server, and you would like to make it automatically visible to existing software in the HAPI ecosystem, please post an [issue with your server URL](https://github.com/hapi-server/servers/issues).

# Legacy Files

Nightly, a process generates the legacy `all.txt` and `all_.txt` files using the content of `abouts.json`.

* `all.txt` - List of production HAPI servers (legacy file)
* `all_.txt` - Additional information about servers. To use until we have developed a schema for such information. (legacy file)
* `dev.txt` - List of HAPI servers under development and not production-ready
