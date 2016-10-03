## drones as a service (daas)
Welcome! This repository is home to a daas marketplace, with a catch: user
reputations are stored in a block-chain.

To check out our project locally:

1. install `docker` ([https://www.docker.com/](https://www.docker.com/))

2. install `docker-compose`

3. clone our repository `git clone https://github.com/samuelhavron/daas.git`

4. create a `mySQL` database, [following these
instructions](https://github.com/thomaspinckney3/cs4501/blob/master/Project1.md).
you need to hard-code in the password to match our [models db
connection](https://github.com/samuelhavron/daas/blob/master/models/models/settings.py#L75-L83) 

5. `cd daas` and run `docker-compose up`

6. the web front end is available at `http://localhost:8000` on your host (view
in your browser)-- the experience
APIs are at `http://localhost:8001` and the entity/model APIs are at
`http://localhost:8002`.

7. questions? contact us: `{mdk6jd, jat9kf, sgh7cc} @ virginia.edu`
