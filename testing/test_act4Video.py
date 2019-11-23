#! /usr/bin/python

"""
test_act4Video.py
a test case where a user authenticates and uploads a new video, accesses their
video, and then deletes it.
"""

import sys, requests, pytest, json


HOST = "http://127.0.0.1"

#a test case that logs into the application successfully
def test_valid_login(s):
    print("[*] Testing login..")

    creds = {'username' : 'brendy', 'password' : 'flannle'}
    s.post((f"{HOST}/login", creds)
    #logged in! cookies saved for future requests.
    r = s.get(f"{HOST}/")
    assert r.status_code == 200
    assert r.url == f"{HOST}/"


if __name__ == "__main__":
    s = requests.session()
    test_valid_login(s)

