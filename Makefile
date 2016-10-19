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
	sudo docker-compose up

hardrun:
	sudo docker rm web
	sudo docker rm models
	sudo docker rm exp
	sudo docker-compose up

database: clean
	sudo docker pull mysql:5.7.14
	mkdir db
	sudo docker run --name mysql -d -e MYSQL_ROOT_PASSWORD='$$3cureUS' -v `pwd`/db:/var/lib/mysql mysql:5.7.14
	sleep 20 # need to give time for mysql to start... :-)
	sudo docker run -it --name mysql-cmd --rm --link mysql:db mysql:5.7.14 \
    mysql -uroot -p'$$3cureUS' -h db -e \
    "CREATE DATABASE cs4501 CHARACTER SET utf8; \
    CREATE DATABASE test_cs4501 CHARACTER SET utf8; \
    CREATE USER 'www'@'%' IDENTIFIED BY '$$3cureUS'; \
    GRANT ALL PRIVILEGES ON *.* TO 'www'@'%';"
 
clean:
	sudo rm -rf db

daas.zip:
	zip -9r daas.zip *
