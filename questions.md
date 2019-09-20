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
We chose to use pytest becuase it was recommended in the project document, some team members were already familiar with it, and it was simple to set up and use.

vim:syn=markdown

