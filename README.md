# To build (with new Postgres Docker):

docker volume create --name=ghtsdata
docker-compose up --build
docker-compose run web python manage.py migrate
docker-compose run web python manage.py createsuperuser
docker-compose run web python manage.py collectstatic --noinput


# To run:
docker-compose up