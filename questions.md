CSEC380 Project Questions
=========================

# Activity 1

## What is the URL of your Github project?
https://github.com/CSEC380-Group-12/CSEC380-Final-Project

## How did you breakup your projects and what are the security ramifications?
We made each activity an epic and broke each epic down into individual user stories. One possible security ramification of this is that developers are now free to work on different stories independently. This has the danger of potentially leading to a breakdown in communication, leading to ambiguity about the interfaces between different aspects of the project, which in turn can lead to security issues. One possible way to rectify this is to have strict, well defined interfaces between the different parts of the project that are universally agreed upon and understood.

## How did you choose to break down your Epic into various issues (tasks)?
We looked at the project document and decided to make each activity its own epic. We then read the goals for each activity and broke them down into their separate logical pieces. For instance: activity 3 was broken down into three logical pieces: logging in, logging out, and answering the activity's questions. Each logical piece became its own user story. The individual requirements for each user story became an acceptance criterium for that story.

## How long did you assign each sprint to be?
Two weeks.

## Did you deviate from the Agile methodology at all? If yes, what is your reasoning for this?
We have not substantially deviated from the Agile methodology thus far.

## How do you ensure that after each issue/milestone that security has been verified? How would you identify such issues in an ideal environment?
We require each merge request to be reviewed and approved by at least one developer who did not work on it originally. In an ideal environment, we would do full security audits of the entire project frequently, preferably at the end of each sprint.

# Activity 2
## What Web Application security mechanisms are involved in your topology? What security mechanisms would ideally be involved?
We used containers for privilege separation of different daemons and services. Idealy, we would use TLS, firewalls, mandatory access control, and OpenBSD.

## What testing framework did you choose and why?
For testing our project, we chose [pytest testing framework](https://pytest.org/en/latest/) because:
- pytest makes it easy to write tests and it's scalable 
- it's easy to integrate with [TravicCI](https://travis-ci.com)
- extensive documentation
- Detailed info on failing assert statements

# Activity 3
## Provide a link to the test cases you generated for this activity.
https://github.com/CSEC380-Group-12/CSEC380-Final-Project/blob/master/testing/act3Login.py
https://github.com/CSEC380-Group-12/CSEC380-Final-Project/blob/master/testing/test_act3Login.py

## How do you ensure that users that navigate to the protected pages cannot bypass authentication requirements?
For each user that successfully authenticates, we create a Flask session. When a user attempts to connect to the protected pages, we check the Flask session to ensure that the user has authenticated. If the user has not authenticated, he is redirected to the login page.

## How do you protect against session fixation?
We use Flask session cookies, which are only sent when a user correctly authenticates and is removed instantly when the user is no longer authenticated.

From our code:
```python
flask session init
app.secret_key = secrets.token_bytes(64)
```

![Burp](https://user-images.githubusercontent.com/29110777/69473685-13aae600-0d85-11ea-8d7b-804a06e465f6.png)

## How do you ensure that if your database gets stolen passwords aren’t exposed?
We hash our passwords for storage in the database.

## How do you prevent password brute force?
There is a login attempt limiter, preventing brute force attacks:

From our code:

```python
rate limit for password brute force
limiter = Limiter(
	app,
	key_func=get_remote_address,
	default_limits=["1000 per day", "60 per hour", "5 per minute"]
)
```

## How do you prevent username enumeration?
When you have a failed login attempt, the generated error message does not differentiate between an incorrect username, password, or both being incorrect.

## What happens if your sessionID is predictable, how do you prevent that?
The sessionID is an extremely convoluted randomly generated string, making it exceedingly difficult to predict and be taken advantage of by an attacker to gain unauthorized access. If it were predictable, it would be possible for an attacker to hijack users' sessions.

# Activity 4
## How do you prevent XSS is this step when displaying the username of the user who uploaded the video?
We sanitize almost all inputs to the database to ensure that nothing malicious can be entered, intentionally or unintentionally.

## How do you ensure that users can’t delete videos that aren’t his own?
The method that is called when deleting a video checks the userID of the currently logged in user and the userID of the video uploader, and if they do not match, you cannot delete the video.

# Activity 5
## How would you fix your code so that these issues were no longer present?
We would change it to use prepared statements (like we did throughout the rest of the code) instead of concatenating the username with the SQL statement.

## What are the limitations, if any that, of the SQL Injection issues you’ve included? 
Since PyMySQL does not allow for multiple statements in a single `execute()` call, this vulnerability is limited to allowing for manipulation of the existing `SELECT` statement; we can not execute any data manipulation statements; however, we can execute other SELECT queries and the like via UNION attacks.

# Activity 6
## How would you fix your code so that this issue is no longer present?

## How does your test demonstrate SSRF as opposed to just accessing any old endpoint.

# Activity 7
## How would you fix your code so that this issue is no longer present?
When uploading files, we specifically stopped sanitizing the input so that it's just the filename put in by the user, but instead we could replace the filename generation with:

```python
filename = secure_filename(fp.filename)
```

Specifically, we would revert commit c886402b360c1e0a5ca469c487dc147ba276d068. This is the same way we did it in earlier, more secure versions of this code.

vim:syn=markdown

