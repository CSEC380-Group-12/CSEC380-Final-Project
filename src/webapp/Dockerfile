# Dockerfile for Flask web server
# Set Python 3.6 Alpine base image
#FROM python:3.6-alpine
# FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
FROM python:3.7.2-stretch


# The WORKDIR directive defines the working directory for the container.
WORKDIR /webapp

# Set up project
ADD . /webapp

# # set path
# ENV PYTHONPATH "${PYTHONPATH}:/"
# ENV STATIC_URL /static
# ENV STATIC_PATH /webapp/static

# Install the dependencies
RUN pip3 install -r requirements.txt

# # Install image preview generator tools
# RUN apk add --no-cache file
# ENV MAGICK_HOME=/usr
# RUN apk add --no-cache imagemagick && \
# apk add --no-cache imagemagick-dev

# Expose the default Flask port
# EXPOSE 5000
# # Run Flask
ENTRYPOINT env FLASK_APP=main.py flask run --host=0.0.0.0


