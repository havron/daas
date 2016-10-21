.PHONY: github run hardrun database clean
MSG=small edit
github:
	git add -A 
	git commit -m "${MSG}"
	git push

run:
	touch web/web/wsgi.py
	touch models/models/wsgi.py
	touch exp/exp/wsgi.py
	docker-compose up

hardrun:
	@docker rm web > /dev/null 2>&1 ||:
	@docker rm models > /dev/null 2>&1 ||:
	@docker rm exp > /dev/null 2>&1 ||:
	docker-compose up

database: clean
	docker pull mysql:5.7.14
	mkdir db
	docker run --name mysql -d -e MYSQL_ROOT_PASSWORD='$$3cureUS' -v db:/var/lib/mysql mysql:5.7.14
	sleep 20 # need to give time for mysql to start... :)
	docker run -it --name mysql-cmd --rm --link mysql:db mysql:5.7.14 \
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
	@docker rm web > /dev/null 2>&1 ||:
	@docker rm exp > /dev/null 2>&1 ||:
	@docker rm models > /dev/null 2>&1 ||:
	@docker stop mysql > /dev/null 2>&1 && \
	docker rm mysql > /dev/null 2>&1 ||:
	@rm -rf db > /dev/null 2>&1 ||:
	@rm daas.* > /dev/null 2>&1 ||:

daas.zip:
	git archive --format=zip HEAD -o daas.zip -9v

daas.tar.gz:
	git archive --format=tar.gz HEAD -o daas.tar.gz -9v
