# Dockerfile for Mariadb database server
# Set maridb base image
FROM mariadb:latest

# Copy all of the scripts db_init over. Any *.sql scripts in this directory
# will be run in ls order to initialize the databases.
COPY db_init/* /docker-entrypoint-initdb.d

