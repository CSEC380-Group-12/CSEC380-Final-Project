Application Interface Definitions
=================================

# Log In

1. Submit a login request from the front end to the back end. This request must
be a HTTP POST request to `/login` with the following paramaters:

```
POST /login
username=<USERNAME>
password=<PASSWORD>
```

2. The back end responds to the post POST request indicating whether or not the
login succeeded, with the following data:

```
status=success|failure
set SESSION_COOKIE_NAME if status == success
```

# Log Out

1. Submit a logout request from the front end to the back end. This request must
be a HTTP POST request to `/logout` with the following paramaters:

```
POST /logout
SESSION_COOKIE_NAME
```

2. The back end responds to the post POST request indicating whether or not the
logout succeeded, with the following data:

```
status=success|failure
clear SESSION_STATUS_COOKIE if status == success
```

vim:syn=markdown

