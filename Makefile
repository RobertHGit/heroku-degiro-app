commit:
	git add .
	git commit -am "$m"
	git push heroku master

log:
	heroku logs -a heroku-degiro-scraper --tail

pip:
	pip freeze > requirements.txt