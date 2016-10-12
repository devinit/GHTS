# To build (with development Sqlite3 db):
docker-compose up

# To build (with new Postgres Docker):

docker-compose up
docker-compose run web python manage.py migrate
docker-compose run web python manage.py createsuperuser


# To run:
docker-compose up