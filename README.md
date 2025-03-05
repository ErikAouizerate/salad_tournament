# SETUP

`cp .env.sample .env`
`cp docker-compose.dev.yaml docker-compose.yaml`

## supprimer la bdd

`rm -rf data/db.sqlite3`

## créer un super user

dans le container django/web
`poetry run python manage.py createsuperuser`  
Puis aller sur http://localhost:8888/admin/

## seed

dans le container django/web
`poetry run python manage.py seed_players`

pour cleaner :
`poetry run python manage.py clean`

# swagger

verifier que dans le `docker-compose.yml` il y a `DEBUG=true`  
puis aller sur : http://localhost:8888/swagger/

## api resume

http://localhost:8888/badminton/api/pairings?tournament=1&random=aa
