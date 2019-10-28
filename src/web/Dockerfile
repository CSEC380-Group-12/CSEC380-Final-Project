# Dockerfile for Flask web server
# Set Python 3.6 Alpine base image
FROM python:3.6-alpine

# Set up project
COPY webapp /webapp
RUN pip3 install -r /webapp/requirements.txt

# Install image preview generator tools
RUN apk add --no-cache file
ENV MAGICK_HOME=/usr
RUN apk add --no-cache imagemagick && \
apk add --no-cache imagemagick-dev

# Expose the default Flask port
 EXPOSE 5000
# Run Flask
ENTRYPOINT env FLASK_APP=/webapp/main.py flask run --host=0.0.0.0

