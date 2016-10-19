# drones as a service (daas)!:octocat:
[![Build Status](https://travis-ci.org/samuelhavron/daas.svg?branch=master)](https://travis-ci.org/samuelhavron/daas)

Welcome! This repository is home to a daas marketplace, with a catch: user
reputations are (will be) stored in a cryptopgraphic block-chain. The marketplace is built on 4
[dockerized](https://www.docker.com/what-docker) tiers: a `mySQL` database, a models/entity API,
an experience service API, and a bootstrap-powered HTML front-end (the latter
three built on separate `django` projects). The tiers interact via `http/json`
requests and responses (only the models API can talk to the database, only the experience API
can talk to the models, etc); we intentionally implement this marketplace as a set
of isolated microservices. Static content for the HTML front-end is currently
served with Django's `whitenoise` wrapper for the Python `wsgi` interface.

To check out our project locally (on your desktop/laptop):

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
