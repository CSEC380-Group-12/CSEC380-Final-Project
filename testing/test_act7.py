#! /usr/bin/python

"""
test_act4Video.py
a test case where a user authenticates and uploads a new video, accesses their
video, and then deletes it.
"""

import sys, requests, pytest, json


HOST = "http://127.0.0.1"

s = requests.session()

# a test case that logs into the application successfully
def test_valid_login():
    print("[*] Testing login..")

    username = 'brendy'
    password = 'flannle'
    s.auth = (username, password)
    creds = {'username' : username, 'password' : password}
    r = s.post(f"{HOST}/login", creds)
    print(f"r: {r}, s: {s}", flush=True)
    # logged in! cookies saved for future requests.
    # r = s.get(f"{HOST}/")
    assert r.status_code == 200
    assert r.url == f"{HOST}/"

def test_video_upload():
    url = "https://secbytes.net/CSEC380/*.mp4"
    data = {'file.URL' : url}
    r = s.post(f"{HOST}/upload", data=data)
    assert r.status_code == 200

def test_video_playback():
    data = {'vidTitle' : "*"}
    r = s.get(f"{HOST}/static/uploads/*.mp4", data=data)
    assert r.status_code == 200

def test_video_delete():
    r = s.get(f"{HOST}/delete/1")
    assert r.status_code == 200
    r = s.get(f"{HOST}/static/vidoPlayer/1")
    assert r.status_code != 200
    r = s.get(f"{HOST}/static/uploads/woff.mp4")
    assert "woff.mp4" not in r.text
    # verify if the video is deleted
