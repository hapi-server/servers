# Server Lists

This repository contains lists of HAPI servers. The master lists are

* `servers.json` - Production servers
* `servers-dev.json` - In-development servers

These files are updated every hour and on each commit. The update involves replacing existing information for each server with responses from an `/about` request (if this endpoint is supported). The code that does this is `src/update-servers-json.py`.

These files should be accessed via
* https://hapi-server.org/servers.json
* https://hapi-server.org/servers-dev.json

Lists in legacy format are:

* `all.txt` - List of URLs for production servers
* `all_.txt` - List of URLs for production servers and additional server metadata
* `dev.txt` - List of URLs for in-development servers

These files are updated when there are changes to `servers.json` or `servers-dev.json`.

# Adding a Server

If you have developed a HAPI server and you would like to make it automatically visible to existing software in the HAPI ecosystem, please make a pull request that adds your server URL to `servers-dev.json` at https://github.com/hapi-server/servers.

We recommend running tests using the [verifier](https://hapi-server.org/verify/) before submitting a pull request. After the pull request is accepted, it will be visible at https://hapi-server.org/servers-dev.json and by the web client [servers-dev](https://hapi-server.org/servers-dev/), and we will run tests with existing HAPI client software.

When the server has been tested and is ready for production use, it will be added to `servers.json` where it will be visible at [servers.json](https://hapi-server.org/servers.json), https://hapi-server.org/servers/, and the client software listed at [Github](https://github.com/hapi-server?q=client-*&type=all).

# Metadata Lists

All metadata from all HAPI servers listed in [servers.json](https://hapi-server.org/servers.json) is available at [all.json](https://hapi-server.org/metadata.json) with the exception of `bins["centers"]` and `bins["ranges"]` if they are arrays.
