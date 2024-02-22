# Lists

This repository contains lists of HAPI servers. The master lists are

* `all.json` - Production servers
* `dev.json` - In-development servers

These files are updated every hour and on each commit by replacing existing information with responses from an `/about` request (for servers that support his endpoint).

Lists in legacy format are:

* `all.txt` - List of URLs for production servers
* `all_.txt` - List of URLs for production servers and additional server metadata
* `dev.txt` - List of URLs for in-development servers

These files are updated when there are changes to `all.json` or `dev.json`.

# Adding a Server

If you have developed a HAPI server and you would like to make it automatically visible to existing software in the HAPI ecosystem, please make a pull request that adds your server URL to `dev.json` at https://github.com/hapi-server/servers. We recommend running tests using https://hapi-server.org/verifier before submitting a pull request.

After the pull request is accepted, it will be visible at https://hapi-server.org/dev.json and https://hapi-server.org/servers-dev, and we will run tests with existing HAPI client software. We will then add the server to `all.json,` where it will be visible at https://hapi-server.org/all.json and https://hapi-server.org/servers, and the client software listed at https://github.com/hapi-server?q=client-*&type=all.