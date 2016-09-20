.PHONY: github
MSG=small edit
# add a human-readable timestamp to the webstats page in a hackish way... :-)
github:
	git add -A 
	git commit -m "${MSG}"
	git push

post:
	python api-posts.py > err.html && google-chrome err.html
