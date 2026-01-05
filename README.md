This repository contains lists of HAPI servers.

* `abouts.json` is the master list. Nightly, a process generates the legacy `all.txt` and `all_.txt` files. Adds new server information to this file and any about information that is not available from the server. Nightly, a process checks the server and over-writes information in this file. 
* `all.txt` - List of production HAPI servers (legacy file)
* `all_.txt` - Additional information about servers. To use until we have developed a schema for such information. (legacy file)
* `dev.txt` - List of HAPI servers under development and not production ready

If you have developed a HAPI server and it is ready for production and you would like to make it automatically visible to existing software in the HAPI ecosystem, please make a pull request that adds your server URL to `dev.txt` at https://github.com/hapi-server/servers. After the pull request is accepted, it will be visible at https://hapi-server.org/servers-dev and we will run tests to verify that existing HAPI software has no issues with the server. At that point, we will move the server URL out of dev.txt and into `all_.txt` at which point it will be visible at https://hapi-server.org/servers and in (at minimum) all of the client software listed at https://github.com/hapi-server?q=client-*&type=all.

# Notes on testing and indexing

Production servers, those listed in all.txt, will be subjected to regular testing and indexing.  Aliveness tests are
run each hour to see that the server is responsive.  This is done by requesting catalogs and downloading an arbitrary
dataset.  Presently this is done using a fixed random hash, so that the same dataset is loaded with each test.  This
is necessary because of the test being particular, and is likely to change.  However, if you would like to improve
testing, note that the test script really needs sampleStartDate and sampleStopDate to be specified, otherwise the test
script is going to guess time intervals several times before it gives up and declares the server broken.

Indexing is done once weekly.  This is a process which from each server downloads the catalog and all info responses.  These
info responses are compiled into a smaller catalog file which contains the parameter names and start and stop dates.  

