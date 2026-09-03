`abouts.json` is the HAPI project's master list of production HAPI servers

`abouts-dev.json` is the HAPI project's master list of development HAPI servers

`abouts-test.json` is the HAPI project's list of servers with data for testing clients

These files should be used by clients.

These files are updated daily based on the files in `defaults/` and the results of an `/about` query. The code that does this is `abouts.py` in the [server-metadata](https://github.com/hapi-server/server-metadata/) repository.

# Adding a Server

The minimal amount of detail is `x_url` and `id`. Choose either of these options to add a server:

* Post an [issue with your server URL](https://github.com/hapi-server/servers/issues)

or

* Edit the appropriate file in `defaults/` by adding an object with at least `x_url` and `id`. 

# Legacy Files

Nightly, a process generates the legacy `all.txt` and `all_.txt` files using the `abouts` files.

* `all.txt` - List of production HAPI servers
* `all_.txt` - Additional information about servers
* `dev.txt` - List of HAPI servers under development and not production-ready
