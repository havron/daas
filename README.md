## drones as a service (daas)
Welcome! This repository is home to a daas marketplace, with a catch: user
reputations are stored in a block-chain. The marketplace is built on 4
dockerized (isolated Linux containers) tiers: a `mySQL` database, a models/entity API,
an experience service API, and a bootstrap-powered HTML front-end (the latter
three built on separate `django` projects). The tiers interact via `http/json`
requests and
responses (only the models API can talk to the database, only the experience API
can talk to the models, etc). Static content for the HTML front-end is currently
served with Django's `whitenoise` wrapper for the app's `wsgi` interface.

To check out our project locally:

1. install `docker` ([https://www.docker.com/](https://www.docker.com/))

2. install `docker-compose`

3. clone our repository `git clone https://github.com/samuelhavron/daas.git`

4. this is the tricky part: you need to create a `mySQL` database with `docker`
and initialize it properly, [following these
instructions](https://github.com/thomaspinckney3/cs4501/blob/master/Project1.md).
hard-code in the password to match our [models db
connection](https://github.com/samuelhavron/daas/blob/master/models/models/settings.py#L75-L83).
ensure the directories you are using are consistent with your local paths. once
your db is setup, it will be pre-loaded with fixtures (test/dummy data) when you
stand the docker containers up -- so you
can interact with a "living" site.

5. `cd daas` and run `docker-compose up`

6. the web front end is available at `http://localhost:8000` on your host (view
in your browser)-- the experience
APIs are at `http://localhost:8001` and the entity/model APIs are at
`http://localhost:8002`.

7. questions? contact us: `{mdk6jd, jat9kf, sgh7cc} @ virginia.edu`

### usage notes
* if any of the `django` containers exit when you stand them up, run `touch 
<container_name>/<container_name>/wsgi.py` to modify their timestamp and force
`docker` to reload them.
