# drones as a service (daas)!:octocat:
[![Build Status](https://travis-ci.org/samuelhavron/daas.svg?branch=master)](https://travis-ci.org/samuelhavron/daas)
[![GitHub release](https://img.shields.io/github/release/samuelhavron/daas.svg)](https://github.com/samuelhavron/daas/releases/latest)
<p align="left">
<img src="https://cdn.rawgit.com/samuelhavron/daas/master/web/daasapp/static/images/home/logo.svg" width="350">
</p>

Welcome! This repository is home to a daas marketplace, built on multiple
[dockerized](https://www.docker.com/what-docker) tiers, including: 
a `mySQL` database, a models/entity API,
an experience service API, and a bootstrap-powered HTML front-end (the latter
three built on separate `django` projects). The tiers interact via `http/json`
requests and responses (only the models API can talk to the database, only the experience API
can talk to the models, etc); we intentionally implement this marketplace as a set
of isolated microservices. Static content for the HTML front-end is currently
served with Django's `whitenoise` wrapper for the Python `wsgi` interface.

## Features (not comprehensive or exhaustive!)
- Multiple [HAProxy](http://www.haproxy.org/) load balancers are used to forward
traffic to instances of each app tier.
- Entries to our `elasticsearch` engine are queued with [Spotify's kafka
  image](https://hub.docker.com/r/spotify/kafka/)
- Every push to GitHub triggers a [Travis CI
  build](https://travis-ci.org/samuelhavron/daas), where our project is built
  from vanilla and our unit tests
  (models/db) and integration tests (selenium/end-to-end web) are automatically
  run and verified for passing.
- This repository has been successfully deployed to a public cloud provider
  (DigitalOcean) as a proof-of-concept; many security features necessary for
  production were implemented.
- We are currently working on adding a map/reduce job with Apache Spark to
  create a recommendation system for users of the site.

## How to run the site
To check out our project locally (on your desktop/laptop; `docker` requires root access):

1. install `docker`: [https://www.docker.com/](https://www.docker.com/)

2. install `docker-compose`: [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

3. clone our repository: `git clone https://github.com/samuelhavron/daas.git`

4. create a `mySQL` database using `docker`: run the command `make database`
([see our Makefile for creation details](https://github.com/samuelhavron/daas/blob/master/Makefile)).
using that setup will hard-code in a database user and password to match our [models db
connection](https://github.com/samuelhavron/daas/blob/master/models/models/settings.py#L97-L105).
the database will be loaded with fixtures (test/dummy data) when you stand the
`docker` containers up -- so you can interact with a "living" site.

5. run `docker-compose up` to start the marketplace!

6. the web front end is available at [http://localhost:8000](http:localhost:8000) 
on your host (view in your browser). the experience
APIs are at [http://localhost:8001](http://localhost:8001) and 
the entity/model APIs are at [http://localhost:8002](http://localhost:8002) 
(however, they only communicate with JSON responses).

7. have questions? contact us! `{mdk6jd, jat9kf, sgh7cc} @ virginia.edu`

### usage notes
* if any of the `django` containers exit unexpectedly when you stand them up, run 
`touch <container_name>/<container_name>/wsgi.py` to modify their timestamp and force
`docker` to reload them.
* if you are already using `docker` and have one or more containers running with
an alias matching one of `{web, exp, models, mysql}`, you may need to rename
your container(s) or those affected in this repository (to do that, simply
change the `container_name` appropriately in
[docker-compose.yml](https://github.com/samuelhavron/daas/blob/master/docker-compose.yml).
to change the `mysql` alias, edit `external_links` in
[docker-compose.yml](https://github.com/samuelhavron/daas/blob/master/docker-compose.yml)
appropriately as well as renaming the container in the 
targets of the
[Makefile](https://github.com/samuelhavron/daas/blob/master/Makefile). a simple
`sed` expression can be used to automate the process.
### HAProxy load balancers (round-robin)
Load balancers for each app tier powered by [HAProxy](http://www.haproxy.org/)'s
[docker build](http://hub.docker.com/_/haproxy/). Cookie-based policies 
(e.g. return users to same servers for caching purposes) is currently 
not enabled; load balancing is purely round-robin style. 
In actual production, Docker Swarm would (should) be
used, and could leverage `docker-compose`'s `scale` feature (currently
not used, app servers are fully enumerated and handled by respective load
balancers).
