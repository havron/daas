.PHONY: github zip touch run
MSG=small edit
github:
	git add -A 
	git commit -m "${MSG}"
	git push

zip:
	zip -9r daas.zip *

touch:
	touch web/web/wsgi.py
	touch models/models/wsgi.py
	touch exp/exp/wsgi.py

run: touch
	sudo docker-compose up

hardrun: 
	sudo docker rm app_web_1
	sudo docker rm app_models_1
	sudo docker rm app_exp_1
	make run
