# To build (with new Postgres Docker):

1. docker volume create --name=ghtsdata
2. docker-compose up --build
3. docker-compose run web python manage.py migrate
4. docker-compose run web python manage.py createsuperuser
5. docker-compose run web python manage.py collectstatic --noinput


# To run:
docker-compose up