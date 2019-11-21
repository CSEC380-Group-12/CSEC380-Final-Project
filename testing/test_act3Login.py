#! /usr/bin/python

"""
test_act3Login.py: test the content/body of an HTML page
Author: Brendan
"""

from lxml import html
import requests
import pytest
import time

def test_login():
    print("Connecting to site...")
    body = html.parse('http://localhost:80').xpath('//body')[0].text_content()
    assert "Username" in body.strip()
    
    print("Connected!\n")
    print("Logging In: Username = brendy, Pass = flannle")
    loginInfo = {"username": "brendy", "password": "flannle"}
    req = requests.post('http://localhost:80/login', data=loginInfo)
    while(req.status_code != 200):
        time.sleep(1)
    assert "UPLOAD" in req.text
    
    print("Logged In!\n")
    print("Attempting Wrong Pass: Username = brendy, Pass = wrongPass...")
    data = {"username": "brendy", "password": "wrongPass"}
    req = requests.post('http://localhost:80/login', data=data)
    while(req.status_code != 200):
        time.sleep(1)
    assert "doesn't exist" in req.text
    
    print("Log in Failed:\n")
    
    print("Attempting Wrong Username: Username = brendy1, Pass = flannle")
    data = {"username": "brendy1", "password": "flannle"}
    req = requests.post('http://localhost:80/login', data=data)
    while(req.status_code != 200):
        time.sleep(1)
    print("Log in Failed\n")
    
    print("End of Test")
    assert "doesn't exist" in req.text

if __name__ == '__main__':
    test_login()
