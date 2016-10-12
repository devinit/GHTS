# start with a base image
FROM django:1.10.1-python2
MAINTAINER vagrant <Alex Miller, alex.miller@devinit.org>

RUN mkdir /src
ADD ./ /src

WORKDIR /src
# install dependencies
RUN apt-get update
RUN pip install -r requirements.txt
RUN python manage.py migrate --noinput
RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'temporary')" | python manage.py shell
RUN python manage.py collectstatic --noinput


CMD gunicorn -w 2 -b 0.0.0.0:8080 ghts.wsgi
