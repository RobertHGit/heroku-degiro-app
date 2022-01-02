requirements:
	pip freeze > requirements.txt

commit:
	git add .
	git commit -am "$m"
	git push

log:
	heroku logs -a heroku-degiro-scraper --tail

running:
	heroku ps:scale worker=1
