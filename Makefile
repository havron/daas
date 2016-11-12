.PHONY: github run dev database clean shell
MSG=small edit
dev:
	sudo docker-compose down
	sudo docker-compose up

github:
	git add -A 
	git commit -m "${MSG}"
	git push

run:
	touch web/web/wsgi.py
	touch models/models/wsgi.py
	touch exp/exp/wsgi.py
	sudo docker-compose up

shell: database
	@sudo docker rm shell > /dev/null 2>&1 ||:
	sudo docker run -it --name shell --link mysql:db -p 8000:8000 -v `pwd`:/app tp33/django

database: clean
	sudo docker pull mysql:5.7.14
	mkdir db
	sudo docker run --name mysql -d -e MYSQL_ROOT_PASSWORD='$$3cureUS' -v `pwd`/db:/var/lib/mysql mysql:5.7.14
	sleep 45 # need to give time for mysql to start... :)
	sudo docker run -it --name mysql-cmd --rm --link mysql:db mysql:5.7.14 \
          mysql -uroot -p'$$3cureUS' -h db -e \
          "CREATE DATABASE cs4501 CHARACTER SET utf8; \
          CREATE DATABASE test_cs4501 CHARACTER SET utf8; \
          CREATE USER 'www'@'%' IDENTIFIED BY '\$$3cureUS'; \
          GRANT ALL PRIVILEGES ON *.* TO 'www'@'%';"

# if you encounter ERROR 2003 (HY000): Can't connect to MySQL server on 'db' (111):
# increase the sleep time. this *likely* occured because the db docker container 
# did not have enough time to complete setting up a mysql community server.

clean:
	@echo "cleaning..." 
	@sudo docker stop mysql > /dev/null 2>&1 && \
	 sudo docker rm mysql > /dev/null 2>&1 ||:
	@sudo rm -rf db > /dev/null 2>&1 ||:
	@sudo docker rm `sudo docker ps -aq` > /dev/null 2>&1 ||:
	@rm daas.* > /dev/null 2>&1 ||:

daas.zip:
	git archive --format=zip HEAD -o daas.zip -9v

daas.tar.gz:
	git archive --format=tar.gz HEAD -o daas.tar.gz -9v
