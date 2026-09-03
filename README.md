`defaults/abouts.json` is the HAPI project's master list of production HAPI servers.

`defaults/abouts-dev.json` is the HAPI project's master list of development HAPI servers.

`defaults/abouts-test.json` is the HAPI project's list of servers with data for testing clients.

Nightly, the about information in the `defaults` files is updated using an `/about` request. The amended files are

`abouts.json`

`abouts-dev.json`

`abouts-test.json`

These amended files should be used by clients.

The code that amends the `default` files is `abouts.py` in the [server-metadata](https://github.com/hapi-server/server-metadata/) repository.

# Adding a Server

Make a pull request or post an [issue with your server URL](https://github.com/hapi-server/servers/issues)

Edit the appropriate file in `defaults/`. The minimal amount of detail is `x_url` and `id`.

# Legacy Files

Nightly, a process generates the legacy `all.txt` and `all_.txt` files using the `abouts` files.

* `all.txt` - List of production HAPI servers
* `all_.txt` - Additional information about servers
* `dev.txt` - List of HAPI servers under development and not production-ready
