# HAProxy load balancers (round-robin)
Load balancers for each app tier powered by [HAProxy](http://www.haproxy.org/)'s
[docker build](http://hub.docker.com/_/haproxy/). Cookie-based policies 
(e.g. return users to same servers for caching purposes) is currently 
not enabled; load balancing is purely round-robin style. 
In actual production, Docker Swarm would (should) be
used, and could leverage `docker-compose`'s `scale` feature (currently
not used, app servers are fully enumerated and handled by respective load
balancers).
