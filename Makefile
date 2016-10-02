.PHONY: github zip
MSG=small edit
github:
	git add -A 
	git commit -m "${MSG}"
	git push

zip:
	zip -9r daas.zip *
