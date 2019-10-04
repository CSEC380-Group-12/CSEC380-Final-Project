# Dockerfile for Flask web server
# Set Python 3.6 Alpine base image
FROM python:3.6-alpine

COPY webapp /webapp
RUN pip3 install -r /webapp/requirements.txt
EXPOSE 5000
#ENTRYPOINT /bin/sh
ENTRYPOINT env FLASK_APP=/webapp/main.py flask run --host=0.0.0.0

