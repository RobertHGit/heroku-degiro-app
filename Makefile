requirements:
	pip freeze | sed '/degiro/d' > requirements.txt
	echo "-e src/" >> requirements.txt

commit:
	git add .
	git commit -am "$m"
	git push

log:
	heroku logs --app heroku-degiro-app-v1 --tail

running:
	heroku ps:scale worker=1 --app heroku-degiro-app-v1

stop:
	heroku ps:scale worker=0 --app heroku-degiro-app-v1

db_info:
	heroku pg:info --app heroku-degiro-app-v1

sql:
	heroku pg:psql --app heroku-degiro-app-v1
