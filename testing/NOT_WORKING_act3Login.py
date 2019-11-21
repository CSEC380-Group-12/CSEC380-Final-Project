#! /usr/bin/python

"""
act3Login.py: test the content/body of an HTML page
Author: Brendan
"""

from lxml import html
import requests
import pytest

HOST = "http://0.0.0.0:80"

def test_login():
    print("Connecting to site...")
    body = html.parse().xpath('//body')[0].text_content()
    assert "Username" in body.strip()
    print("Connected!\n")
  
    print("Logging In: Username = brendy, Pass = flannle")
    loginInfo = {"username": "brendy", "password": "flannle"}
    req = requests.post(f'{HOST}/login', data=loginInfo)
    assert "UPLOAD" in req.text
    print("Logged In!\n")

    print("Attempting Wrong Pass: Username = brendy, Pass = wrongPass...")
    data = {"username": "brendy", "password": "wrongPass"}
    req = requests.post(f'{HOST}/login', data=data)
    assert "doesn't exist" in req.text
    print("Log in Failed:\n")
    
    print("Attempting Wrong Username: Username = brendy1, Pass = flannle")
    data = {"username": "brendy1", "password": "flannle"}
    req = requests.post('{HOST}/login', data=data)
    assert "doesn't exist" in req.text
    print("Log in Failed\n")
    
    print("End of Test")
    assert "doesn't exist" in req.text


