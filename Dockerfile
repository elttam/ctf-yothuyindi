# NOTE: DO NOT TAG LATEST DOCKER IMAGE. SPECIFY THE VERSION. latest may break in future
FROM python:alpine
#FROM python:3.7.0-alpine3.8

LABEL description="yaml-to-json" \
      maintainer="elttam"

# The flag is in the SECRET_KEY as environment variable. docker-compose can overwrite this value.
ENV SECRET_KEY="libctf{it's a short song but it's a hell of a story}"

# create and copy contents of app to the container
WORKDIR /app
COPY ./app /app

# install and requirements
RUN pip install --no-cache-dir -r requirements.txt

# expose required ports
EXPOSE 8080

# Drop the priviledges for running process otherwise may run as root
USER nobody

# execute
CMD [ "gunicorn", "--workers=2", "--bind=0.0.0.0:8080", "yaml_to_json:create_app()" ]
