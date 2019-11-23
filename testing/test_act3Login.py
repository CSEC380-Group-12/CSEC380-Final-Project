#! /usr/bin/python

"""
test_act3Login.py: test login
Author: Brendan
"""

from lxml import html
import requests
import pytest

HOST = "http://127.0.0.1"

#a test case that logs into the application successfully
def test_valid_login():
    print("[*] Testing login..")
    creds = {'username' : 'brendy', 'password' : 'flannle'}
    req = requests.post(f"{HOST}/login", creds)
    
    assert req.status_code == 200
    assert req.url == f"{HOST}/"

# a test case that tries to log in with the wrong password and fails.
def test_invalid_password():
    print("[*] Testing invalid password..")
    creds = {'username' : 'brendy', 'password' : 'elnnalf'}
    req = requests.post(f"{HOST}/login", creds)
    assert req.url == f"{HOST}/invalid_login"

# a test case that tries to log in with the wrong username and fails.
def test_invalid_login():
    ("[*] Testing invalid username..")
    creds = {'username' : 'Pablo', 'password' : 'flannle'}
    req = requests.post(f"{HOST}/login", creds)
    assert req.url == f"{HOST}/invalid_login"


    ("[*] Testing invalid username and password..")
    creds = {'username' : 'Pablo', 'password' : 'potato'}
    assert req.url == f"{HOST}/invalid_login"

if __name__ == "__main__":
    test_valid_login()
    test_invalid_login()