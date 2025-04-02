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

GET : http://localhost:8000/badminton/api/tournaments/3/nextRound?random=true&toFinish=true
GET : http://localhost:8000/badminton/api/tournaments/3/missingRounds/

POST : http://localhost:8000/badminton/api/tournaments/3/saveRound/

```json
{
  "round": {
    "results": [
      {
        "teamA": [
          {
            "id": 24
          },
          {
            "id": 33
          }
        ],
        "teamB": [
          {
            "id": 26
          },
          {
            "id": 34
          }
        ],
        "hasTeamAWon": true
      },
      {
        "teamA": [
          {
            "id": 28
          },
          {
            "id": 20
          }
        ],
        "teamB": [
          {
            "id": 27
          },
          {
            "id": 25
          }
        ],
        "hasTeamAWon": true
      },
      {
        "teamA": [
          {
            "id": 22
          },
          {
            "id": 32
          }
        ],
        "teamB": [
          {
            "id": 23
          },
          {
            "id": 21
          }
        ],
        "hasTeamAWon": true
      }
    ]
  },
  "toFinish": false
}
```
