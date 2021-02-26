psql:
	docker-compose exec postgres psql -U django_db_user -p 5432 -h 0.0.0.0 -d django_db
migrate:
	docker-compose exec django python3 manage.py migrate --run-syncdb
migrations:
	docker-compose exec django python3 manage.py makemigrations
migrations-clans:
	docker-compose exec django python3 manage.py makemigrations clans
migrations-accounts:
	docker-compose exec django python3 manage.py makemigrations accounts
user:
	docker-compose exec django python3 manage.py createsuperuser
showmigrations:
	docker-compose exec django python3 manage.py showmigrations
test:
	docker-compose exec django python3 manage.py test
insert:
	docker-compose exec django python3 manage.py loaddata feature_initial.json && docker-compose exec django python3 manage.py loaddata game_initial.json && docker-compose exec django python3 manage.py loaddata question_initial.json
insert-feature:
	docker-compose exec django python3 manage.py loaddata feature_initial.json
insert-game:
	docker-compose exec django python3 manage.py loaddata game_initial.json
insert-faq:
	docker-compose exec django python3 manage.py loaddata question_initial.json